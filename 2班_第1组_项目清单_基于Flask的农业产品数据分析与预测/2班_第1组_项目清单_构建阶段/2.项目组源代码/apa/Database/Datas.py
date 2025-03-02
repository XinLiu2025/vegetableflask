import os
import csv
import pymysql

# MLSQL数据库连接配置
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '20010906xx',
    'database': 'vegview',
    'charset': 'utf8mb4',
}


def write_to_database(file_path, product):
    # 连接到MLSQL数据库
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            with open(file_path, 'r', encoding='utf8') as file:  # 修改了文件编码为 utf-8-sig
                reader = csv.reader(file)
                # 跳过表头
                next(reader)
                row_number = 0
                for row in reader:
                    row_number += 1
                    try:
                        # 将数据插入到数据库中
                        sql = "INSERT INTO product_prices (product, release_date, min_price, avg_price, max_price) VALUES (%s, %s, %s, %s, %s)"
                        cursor.execute(sql, (row[2], row[7], float(row[3]), float(row[4]), float(row[5])))
                        print(f"Row {row_number} inserted successfully!")
                    except Exception as e:
                        print(f"Error inserting row {row_number}: {row}")
                        print(f"Error message: {str(e)}")
            # 提交事务
            connection.commit()
    except Exception as e:
        print(f"Error writing to database: {str(e)}")
    finally:
        connection.close()


def process_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            # 构建完整的文件路径
            file_path = os.path.join(folder_path, file_name)
            # 提取产品名称，假设文件名格式为"产品名称价格.csv"
            product = file_name.split('价格.csv')[0]
            # 调用函数将数据写入数据库
            write_to_database(file_path, product)


# 调用函数处理文件夹中的所有文件
folder_path = "../农产品价格情况/"
process_folder(folder_path)
