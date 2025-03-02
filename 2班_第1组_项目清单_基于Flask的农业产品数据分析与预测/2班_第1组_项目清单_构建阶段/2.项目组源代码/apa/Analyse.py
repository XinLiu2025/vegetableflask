# -*- coding: utf-8 -*-
import csv
import json
import pandas as pd
import numpy as np
import demjson
import os
import pandas as pd
import datetime
from tqdm import tqdm

import numpy as np
# from sklearn.preprocessing import MinMaxScaler
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, LSTM
# import matplotlib.pyplot as plt
import pymysql

# MLSQL数据库连接配置
db_config = {
    'host': '123.56.109.152',
    'port': 3306,
    'user': 'vegview',
    'password': '20010906xx',
    'database': '4kizhmH7BHBYkFk6',
    'charset': 'utf8mb4',
}

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

def analyze_data(folder_path):
    all_products = {}
    for filename in tqdm(os.listdir(folder_path)):
        if filename.endswith('.csv'):
            product = os.path.splitext(filename)[0].split('价格')[0]
            data = get_data_from_database(product)
            max_price = max(entry['max_price'] for entry in data)
            all_products[product] = max_price

    # 根据最高价对商品进行排序
    sorted_products = sorted(all_products.items(), key=lambda x: x[1], reverse=True)

    # 写入CSV文件
    csv_file_path = 'middle/word_cloud_data.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for product, max_price in sorted_products:
            writer.writerow({'name': product, 'value': max_price})

    return csv_file_path

# 测试
folder_path = '农产品价格情况'
csv_file_path = analyze_data(folder_path)
print(f"CSV文件已生成：{csv_file_path}")


import pandas as pd
import os

# 定义文件夹路径
folder_path = '蔬菜价格'  # 将此路径替换为包含CSV文件的文件夹路径

# 用于存储每个CSV文件的品名个数
file_product_counts = []

# 遍历文件夹中的所有CSV文件，并统计每个文件的品名个数
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):  # 确保它是CSV文件
        file_path = os.path.join(folder_path, filename)
        try:
            csv_data = pd.read_csv(file_path)
            unique_product_count = len(set(csv_data['品名']))
            file_product_counts.append({
                'type': filename.split('报价')[0],
                'sums': unique_product_count
            })
        except Exception as e:
            print(f'Error reading {filename}: {e}')

# 将统计结果转换为DataFrame并写入新的CSV文件
result_df = pd.DataFrame(file_product_counts)
output_file = 'middle/product_counts_summary.csv'
result_df.to_csv(output_file, index=False)

print(f'Product counts have been written to {output_file}')