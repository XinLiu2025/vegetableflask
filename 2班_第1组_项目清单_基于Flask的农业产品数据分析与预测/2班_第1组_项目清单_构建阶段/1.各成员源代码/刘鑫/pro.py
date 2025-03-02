# -*- coding: utf-8 -*-
import csv
import json
import pandas as pd
import numpy as np
import demjson
import os
import pandas as pd
import datetime
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
import pymysql
import os
# 获取文件2所在的目录
file_directory = os.path.dirname(__file__)

os.chdir(file_directory)
# MLSQL数据库连接配置
db_config = {
    'host': 'xxxxxxxxxxxx',
    'port': 3306,
    'user': 'xxxxxxxxxxxxxxxxx',
    'password': 'xxxxxxxxxxxxxxxxxxxxx',
    'database': 'vegview',
    'charset': 'utf8mb4',
}


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bytes, np.generic)):
            return str(obj, encoding='utf-8')
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return super().default(obj)
def get_data_from_database(product):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 在SQL查询中添加LIMIT 50来限制返回的记录数
            sql = "SELECT release_date, min_price, avg_price, max_price FROM product_prices WHERE product = %s ORDER BY release_date ASC LIMIT 45"
            cursor.execute(sql, (product,))
            result = cursor.fetchall()
            data = []
            for row in result:
                data.append({
                    'date': row[0].strftime('%Y-%m-%d'),
                    'min_price': row[1],
                    'avg_price': row[2],
                    'max_price': row[3]
                })
            return data
    finally:
        connection.close()





def getdata(product):
    dict_return = {}
    data = get_data_from_database(product)
    file_1 = get_data_from_database(product)

    dates = [entry['date'] for entry in data]
    min_price = [entry['min_price'] for entry in data]
    avg_price = [entry['min_price'] for entry in data]
    max_price = [entry['min_price'] for entry in data]

    avg_price0 = [entry['min_price'] for entry in file_1]
    avg_price1 = [entry['max_price'] for entry in file_1]
    avg_price2 = [entry['avg_price'] for entry in file_1]
    spl = len(avg_price0) // 3
    data_1 = avg_price0[:spl]
    data_2 = avg_price1[spl:spl * 2]
    data_3 = avg_price2[spl * 2:]

    month=dates
    high_price = max_price
    low_price = min_price
    price = avg_price

    dict_return['date'] = month
    dict_return['high_price'] = high_price
    dict_return['price'] = price
    dict_return['low_price'] = low_price

    jsonList = []
    for i in range(0, len(low_price)):
        jsonList.append({'name': month[i], 'value': high_price[i]+1})
    data0 = json.dumps(jsonList, cls=MyEncoder, ensure_ascii=False)
    data0 = demjson.decode(data0)
    dict_return['data0'] = data0

    radar0 = []
    radar1 = [{'value':data_1,'name':month[0]}]
    radar2 = [{'value':data_2,'name':month[5]}]
    radar3 = [{'value':data_3,'name':month[6]}]


    for j in range(0, 8):
        radar0.append({'name': month[j], 'max': max(high_price) +max(high_price)*0.5})
    data1 = json.dumps(radar0, cls=MyEncoder, ensure_ascii=False)
    data1 = demjson.decode(data1)
    dict_return['radar0'] = data1
    dict_return['radar1'] = radar1
    dict_return['radar2'] = radar2
    dict_return['radar3'] = radar3

    item = []
    for i in range(0, len(low_price)):
        item.append({'date': month[i], 'price': price[i], 'high_price': high_price[i], 'low_price': low_price[i]})
    data_tb = json.dumps(item, cls=MyEncoder, ensure_ascii=False)
    data_tb = demjson.decode(data_tb)
    dict_return['data_tb'] = data_tb
    dict_return['n'] = product
    # 统计词云品类
    word = pd.read_csv('middle/word_cloud_data.csv',encoding='utf-8')
    classs = pd.read_csv('middle/product_counts_summary.csv', encoding='utf-8')
    dict_return['word'] = word['name'].tolist()
    dict_return['wordi'] = word['value'].tolist()
    wordcount = []
    for i in range(0, len(dict_return['word'])//3):
        wordcount.append({'name': dict_return['word'][i], 'value': dict_return['wordi'][i]})
    wordcounts = json.dumps(wordcount, cls=MyEncoder, ensure_ascii=False)
    wordcounts = demjson.decode(wordcounts)
    dict_return['words']=wordcounts

    dict_return['class'] = classs['type'].tolist()
    dict_return['classi'] = classs['sums'].tolist()
    classii = []
    for i in range(0, len(dict_return['class'])):
        classii.append({'name': dict_return['class'][i], 'value': dict_return['classi'][i]})
    clas = json.dumps(classii, cls=MyEncoder, ensure_ascii=False)
    clas = demjson.decode(clas)
    dict_return['clas']=clas

    # Treemap
    # 读取CSV文件
    df = pd.read_csv('产地分析/进口果.csv')

    # 组织数据为树形图需要的结构
    data = []
    for location in df['产地'].unique():
        location_data = {'name': location, 'children': []}
        filtered_df = df[df['产地'] == location]
        for fruit in filtered_df['品名'].unique():
            fruit_data = {'name': fruit, 'children': []}
            fruit_details = filtered_df[filtered_df['品名'] == fruit]
            for _, row in fruit_details.iterrows():
                fruit_data['children'].append({
                    'name': f"{row['发布日期']} 均价: {row['平均价']}",
                    'value': row['平均价']
                })
            location_data['children'].append(fruit_data)
        data.append(location_data)

    # 将数据转换为适合前端使用的格式
    dict_return['area'] = data
    return dict_return


def getpredict(product):
    predictdata = {}
    data = get_data_from_database(product)

    date_back = [entry['date'] for entry in data]
    price_back = [entry['avg_price'] for entry in data]
    # 将列表转换为 DataFrame
    date_format = '%Y-%m-%d'
    date_back = pd.to_datetime(date_back,format=date_format)

    df = pd.DataFrame({'发布日期': date_back, '平均价': price_back})
    last_date=date_back.max()
    future_dates = [last_date + datetime.timedelta(days=i) for i in range(1, 8)]

    # 计算日期之间的天数差异
    df['发布日期'] = (df['发布日期'] - df['发布日期'].min()).dt.days
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df[['发布日期', '平均价']])

    X_train = []
    y_train = []
    for i in range(7, len(data)):
        X_train.append(scaled_data[i - 7:i, :])
        y_train.append(scaled_data[i, 1])

    X_train, y_train = np.array(X_train), np.array(y_train)

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 2)))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(units=25))
    model.add(Dense(units=7))

    model.compile(optimizer='adam', loss='mean_squared_error')
    history = model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=0)

    predictdata['loss'] = [round(i, 3) for i in history.history['loss']]

    last_7_days = scaled_data[-7:]
    X_future = np.array([last_7_days])

    X_future = np.reshape(X_future, (X_future.shape[0], X_future.shape[1], 2))

    predicted_prices_scaled = model.predict(X_future)

    predicted_prices_scaled_reshaped = predicted_prices_scaled.reshape(-1, 1)

    predicted_prices_combined = np.concatenate((last_7_days[:, 0].reshape(-1, 1), predicted_prices_scaled_reshaped),
                                               axis=1)

    predicted_prices = scaler.inverse_transform(predicted_prices_combined)[:, 1]

    predicted_prices_future = predicted_prices[-7:]
    # 创建一个DataFrame来存储未来日期和预测价格
    future_price_df = pd.DataFrame({'日期': future_dates, '价格': predicted_prices_future})

    # 打印未来7天的预测价格
    print("未来7天的预测价格:")
    print(future_price_df)

    # 将日期转换回原始格式
    df['发布日期'] = pd.to_datetime(df['发布日期'].min(), format=date_format) + pd.to_timedelta(df['发布日期'], unit='D')

    lida = [i.strftime('%Y-%m-%d') for i in future_dates]
    date_back = [i.strftime('%Y-%m-%d') for i in date_back]

    predictdata['rawdate'] = date_back
    predictdata['newdate'] = date_back + lida
    predictdata['rawprice'] = price_back
    predictdata['newprice'] = price_back + [round(num, 1) for num in predicted_prices_future]
    predictdata['epochs'] = [i for i in range(1, len(history.history['loss']) + 1)]
    predictdata['fudate'] = lida
    predictdata['fuprice'] = [round(i, 3) for i in predicted_prices[-7:]]

    raw_prices = predictdata['rawprice']

    price_frequency = {}
    for price in raw_prices:
        if price not in price_frequency:
            price_frequency[price] = 0
        price_frequency[price] += 1

    sorted_price_frequency = sorted(price_frequency.items())

    price_list = []
    fre_list = []
    for price, frequency in sorted_price_frequency:
        price_list.append(price)
        fre_list.append(frequency)
    predictdata['price_list'] = price_list
    predictdata['fre_list'] = fre_list

    item0 = []
    for i in range(0, len(lida)):
        item0.append({'date': lida[i], 'price': predictdata['fuprice'][i]})
    data_tb = json.dumps(item0, cls=MyEncoder, ensure_ascii=False)
    data_tb = demjson.decode(data_tb)
    predictdata['fup'] = data_tb
    predictdata['n'] = product

    return predictdata



