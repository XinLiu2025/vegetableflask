# # 1、Create Database
#
# import pymysql
#
# # MLSQL数据库连接配置
# db_config = {
#     'host': 'localhost',
#     'port': 3306,
#     'user': 'root',
#     'password': 'root',
#     'charset': 'utf8mb4',
# }
#
# def create_database(database_name):
#     # 连接到MySQL服务器
#     connection = pymysql.connect(**db_config)
#
#     try:
#         with connection.cursor() as cursor:
#             # 创建数据库
#             sql = "CREATE DATABASE IF NOT EXISTS {}".format(database_name)
#             cursor.execute(sql)
#         # 提交事务
#         connection.commit()
#     finally:
#         connection.close()
#     print("Database created!")
# # 调用函数创建数据库
# create_database('vegview')


# 2、Create Table
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
            cursor.execute("DROP TABLE IF EXISTS product_prices")

            # 创建农产品表
            sql = """
                CREATE TABLE product_prices (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product VARCHAR(255) CHARACTER SET utf8mb4,
                    release_date DATE,
                    max_price FLOAT,
                    min_price FLOAT,
                    avg_price FLOAT
                );
            """
            cursor.execute(sql)

            # 创建用户表
            cursor.execute("DROP TABLE IF EXISTS users")
            sql = """
                CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                );
            """
            cursor.execute(sql)

        # 提交事务
        connection.commit()
    finally:
        connection.close()
    print("Tables created!")


# 调用函数创建表
create_table()
