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


def create_table():
    # 连接到MLSQL数据库
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # 如果表存在则删除
            cursor.execute("DROP TABLE IF EXISTS users")

            # 创建用户表
            sql = """
                CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    sex VARCHAR(10),
                    email VARCHAR(255),
                    phone_number VARCHAR(20),
                    birthday DATE
                );
            """
            cursor.execute(sql)
        # 提交事务
        connection.commit()
    finally:
        connection.close()
    print("Users table created!")


def insert_users():
    # 读取CSV文件中的用户数据
    with open('../utils/information.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行
        users_data = list(reader)

    # 连接到MLSQL数据库
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # 插入用户数据到用户表中
            for user_data in users_data:
                sql = "INSERT INTO users (username, password, sex, email, phone_number, birthday) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5]))
            # 提交事务
            connection.commit()
    finally:
        connection.close()
    print("Users inserted into the table!")


# 调用函数创建用户表
create_table()

# 调用函数将用户数据插入到用户表中
insert_users()
