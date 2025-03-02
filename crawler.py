import requests
import csv
import time

LOne = {"蔬菜": 1186, "水果": 1187, "肉禽蛋": 1189,
        "水产": 1190, "粮油": 1188, "豆制品": 1203,
        "调料": 1204}

LTwo = {"水菜": 1199, "特菜": 1200,
        "进口果": 1201, "干果": 1202,
        "猪肉类": 1205, "牛肉类": 1206, "羊肉类": 1207, "禽蛋类": 1208,
        "淡水鱼": 1209, "海水鱼": 1210, "虾蟹类": 1217, "贝壳类": 1218, "其他类": 1211,
        "米面类": 1212, "杂粮类": 1213, "食用油": 1214}

url = "http://www.xinfadi.com.cn/getPriceData.html"

def getcsv(Type1,Type2):
    data = {
        "limit": 200,
        "current": 1,

        # 获取数据时间范围
        "pubDateStartTime": datastart,
        "pubDateEndTime": dataend,

        # 第一大类、第二大类名称
        "prodPcatid": LOne[Type1],
        "prodCatid": LTwo[Type2],
        "prodName": ""
    }
    with open('./蔬菜价格/'+Type2+'报价.csv', mode='w+', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["一级分类", "二级分类", "品名", "最低价", "平均价", "最高价", "单位", "发布日期"])

        response = requests.post(url, data)
        json_data = response.json()
        count = json_data['count']
        limit = json_data['limit']
        n = count // limit + 1

        for i in range(1, n + 1):
            # 避免ip被封及异常
            time.sleep(1)

            data['current'] = i
            response = requests.post(url, data)
            json_data = response.json()['list']
            for e in json_data:
                e1 = e['prodCat']   # "一级分类"
                e2 = e['prodPcat']  # "二级分类"
                e3 = e['prodName']  # "品名"
                e4 = e['lowPrice']  # "最低价"
                e5 = e['avgPrice']  # "平均价"
                e6 = e['highPrice'] # "最高价"

                e9 = e['unitInfo']  # "单位"
                e10 = e['pubDate'].split(' ')[0]  # "发布日期"

                t = [e1, e2, e3, e4, e5, e6,  e9, e10]
                print(t)
                csv_writer.writerow(t)


'''Type1、Type2要对应，否则无数据，对应列表如下：

   Type1                Type2
    蔬菜               水菜、特菜
    水果              进口果、干果
    肉禽蛋       猪肉类、牛肉类、羊肉类、禽蛋类
    水产      淡水鱼、海水鱼、虾蟹类、贝壳类、其他类
    粮油          米面类、杂粮类、食用油

ps：豆制品、调料无二级分类
'''


Type1L = ['蔬菜','水果','肉禽蛋','水产','粮油']
Type2L = [['水菜','特菜'],['进口果','干果'],['猪肉类','牛肉类','羊肉类','禽蛋类'],
          ['淡水鱼','海水鱼','虾蟹类','贝壳类','其他类'],['米面类','杂粮类','食用油']]




# 数据时间范围，格式
datastart = "2020/01/01"
dataend = "2022/01/01"

if __name__ == '__main__':

    # 遍历输出所有类别数据

    # 例，想获取”进口果“数据，Type1=”水果“，Type2=”进口果“，输出文档名称为”进口果报价.csv“
    # Type1 = "水果"
    # Type2 = "进口果"

    # 其中Type1L 代表一级类别所有类型，Type2L亦如是
    for i in range(len(Type1L)):
        Type1 = Type1L[i]
        for j in Type2L[i]:
            Type2 = j
            getcsv(Type1,Type2)


