# -*- coding: utf-8 -*-
import re
from flask import session
from flask import Flask, request, render_template, redirect, url_for
from pro import getdata,getpredict
import secrets
import pymysql
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '20010906xx',
    'database': 'vegview',
    'charset': 'utf8mb4',
}
def get_user_info(username):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 查询用户信息
            sql = "SELECT password FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            if result:
                return result[0]  # 返回密码
            else:
                return None
    finally:
        connection.close()
def check_username_exist(username):
    # 连接到MLSQL数据库
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # 查询数据库中是否存在相同的用户名
            sql = "SELECT * FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            if result:
                return True  # 用户名已存在
            else:
                return False  # 用户名不存在
    finally:
        connection.close()
def save_user_info(username, password, sex, email, phone_number, birthday):
    # 连接到MLSQL数据库
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # 插入用户信息到数据库
            sql = "INSERT INTO users (username, password, sex, email, phone_number, birthday) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (username, password, sex, email, phone_number, birthday))
            # 提交事务
            connection.commit()
    finally:
        connection.close()
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        stored_password = get_user_info(username)
        if stored_password and stored_password == password:
            session['username'] = username  # 在会话中设置用户名
            if 'admin_login' in request.form:
                session['is_admin'] = True  # 在会话中设置管理员标志
            return redirect(url_for('query'))
        else:
            return render_template('login.html', error="Invalid username or password. Please try again.")
    return render_template('login.html')

@app.route('/index', methods=['GET', 'POST'])
def query():
    if request.method == "POST":
        product = request.form.get("product")
        dict_return = getdata(product)
        return render_template('index.html', dict_return=dict_return)
    else:
        dict_return = getdata('北方江米')                       #默认初始页面
        return render_template('index.html', dict_return=dict_return)
@app.route('/chart', methods=['GET', 'POST'])
def chart():
    if request.method == "POST":
        product = request.form.get("product")
        try:
            dict_return = getdata(product)
        except Exception as e:
            # 捕获异常并记录错误信息
            app.logger.error(f"查询失败: {str(e)}")
            # 返回错误页面或错误信息给用户
            return render_template('error.html', error="查询失败，请稍后再试。")
        return render_template('chart.html', dict_return=dict_return)
    else:
        dict_return = getdata('北方江米')                       #默认初始页面
        return render_template('chart.html', dict_return=dict_return)

@app.route('/chart1', methods=['GET', 'POST'])
def chart1():
    if request.method == "POST":
        product = request.form.get("product")
        try:
            dict_return = getdata(product)
        except Exception as e:
            # 捕获异常并记录错误信息
            app.logger.error(f"查询失败: {str(e)}")
            # 返回错误页面或错误信息给用户
            return render_template('error.html', error="查询失败，请稍后再试。")
        return render_template('chart1.html', dict_return=dict_return)
    else:
        dict_return = getdata('北方江米')                       #默认初始页面
        return render_template('chart1.html', dict_return=dict_return)

@app.route('/chart2', methods=['GET', 'POST'])
def chart2():
    if request.method == "POST":
        product = request.form.get("product")
        try:
            dict_return = getdata(product)
        except Exception as e:
            # 捕获异常并记录错误信息
            app.logger.error(f"查询失败: {str(e)}")
            # 返回错误页面或错误信息给用户
            return render_template('error.html', error="查询失败，请稍后再试。")
        return render_template('chart2.html', dict_return=dict_return)
    else:
        dict_return = getdata('北方江米')  # 默认初始页面
        return render_template('chart2.html', dict_return=dict_return, product='北方江米') # 将默认产品名称传递给模板

@app.route('/chart3', methods=['GET', 'POST'])
def chart3():
    if request.method == "POST":
        product = request.form.get("product")
        try:
            dict_return = getdata(product)
        except Exception as e:
            # 捕获异常并记录错误信息
            app.logger.error(f"查询失败: {str(e)}")
            # 返回错误页面或错误信息给用户
            return render_template('error.html', error="查询失败，请稍后再试。")
        return render_template('chart3.html', dict_return=dict_return)
    else:
        dict_return = getdata('北方江米')  # 默认初始页面
        return render_template('chart3.html', dict_return=dict_return, product='北方江米') # 将默认产品名称传递给模板

@app.route('/chart4', methods=['GET', 'POST'])
def chart4():
    if request.method == "POST":
        product = request.form.get("product")
        try:
            dict_return = getdata(product)
        except Exception as e:
            # 捕获异常并记录错误信息
            app.logger.error(f"查询失败: {str(e)}")
            # 返回错误页面或错误信息给用户
            return render_template('error.html', error="查询失败，请稍后再试。")
        return render_template('chart4.html', dict_return=dict_return)
    else:
        dict_return = getdata('北方江米')  # 默认初始页面
        return render_template('chart4.html', dict_return=dict_return, product='北方江米') # 将默认产品名称传递给模板

@app.route('/chart5', methods=['GET', 'POST'])
def chart5():
    if request.method == "POST":
        product = request.form.get("product")
        try:
            dict_return = getdata(product)
        except Exception as e:
            # 捕获异常并记录错误信息
            app.logger.error(f"查询失败: {str(e)}")
            # 返回错误页面或错误信息给用户
            return render_template('error.html', error="查询失败，请稍后再试。")
        return render_template('chart5.html', dict_return=dict_return)
    else:
        dict_return = getdata('北方江米')  # 默认初始页面
        return render_template('chart5.html', dict_return=dict_return, product='北方江米') # 将默认产品名称传递给模板


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == "POST":
        product = request.form.get("product")
        try:
            predictdata = getpredict(product)
        except Exception as e:
            app.logger.error(f"查询失败: {str(e)}")
            # 返回错误页面或错误信息给用户
            return render_template('error.html', error="查询失败，请稍后再试。")
        return render_template('predict.html', predictdata=predictdata, product=product)
    else:
        predictdata = getpredict('金龙鱼大豆油')
        return render_template('predict.html', predictdata=predictdata, product='金龙鱼大豆油')

@app.route('/register', methods=['GET', 'POST'], endpoint='register')
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        sex = request.form.get('sex')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        birthday = request.form.get('birthday')
        # 检查用户名是否已存在
        if check_username_exist(username):
            error = '用户名已存在，请选择其他用户名'
            return render_template('register.html', error=error)

        # 密码强度校验
        if not re.search(r'[a-z]', password) or not re.search(r'[A-Z]', password) or not re.search(r'[0-9]', password):
            return '密码必须包含大小写字母和数字'

        try:
            save_user_info(username, password, sex, email, phone_number, birthday)
            x = f'{username}注册成功'
        except:
            error = '注册失败，请检查用户是否已经存在'
            return render_template('register.html', error=error)

        return render_template('login.html', x=x)
    else:
        return render_template('register.html')
# 用户管理路由
@app.route('/manage')
def manage():
    if session.get('is_admin'):
        users = get_all_users()
        return render_template('manage.html', users=users)
    else:
        return render_template('access_denied.html')
@app.route('/user/add', methods=['POST'])
def add_user():
    username = request.form.get('username')
    password = request.form.get('password')
    sex = request.form.get('sex')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    birthday = request.form.get('birthday')

    # 检查用户名是否已存在
    if check_username_exist(username):
        error = '用户名已存在，请选择其他用户名'
        users = get_all_users()
        return render_template('manage.html', users=users, error=error)

    # 添加用户
    try:
        save_user_info(username, password, sex, email, phone_number, birthday)
    except:
        error = '添加用户失败，请检查用户是否已经存在'
        users = get_all_users()
        return render_template('manage.html', users=users, error=error)

    return redirect(url_for('manage'))

@app.route('/delete/<username>', methods=['POST'])
def delete_user(username):
    # 删除用户
    # 这里可以加入确认删除的逻辑，以避免误操作
    users = get_all_users()
    updated_users = [user for user in users if user['username'] != username]

    # 重新写入数据库
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 先清空表
            cursor.execute("TRUNCATE TABLE users")
            # 重新插入数据
            for user in updated_users:
                sql = "INSERT INTO users (username, password, sex, email, phone_number, birthday) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (user['username'], user['password'], user['sex'], user['email'], user['phone_number'], user['birthday']))
            # 提交事务
            connection.commit()
    finally:
        connection.close()

    return redirect(url_for('manage'))
def get_all_users():
    # 连接到数据库
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 执行查询所有用户的SQL语句
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            # 获取所有用户的数据
            users = cursor.fetchall()
            # 将查询结果转换为字典列表
            user_list = []
            for user in users:
                user_dict = {
                    'username': user[1],
                    'password': user[2],
                    'sex': user[3],
                    'email': user[4],
                    'phone_number': user[5],
                    'birthday': user[6]
                }
                user_list.append(user_dict)
    finally:
        # 关闭数据库连接
        connection.close()

    return user_list
@app.route('/products', methods=['GET', 'POST'])
def products():
    page = request.args.get('page', 1, type=int)
    page_size = 5
    search_query = request.args.get('search', '')  # 接受搜索参数
    if not session.get('is_admin'):
        return render_template('access_denied.html')

    if request.method == 'POST' and 'add' in request.form:
        # 添加产品逻辑
        product = request.form.get('product')
        release_date = request.form.get('release_date')
        min_price = request.form.get('min_price')
        avg_price = request.form.get('avg_price')
        max_price = request.form.get('max_price')
        add_product(product, release_date, min_price, avg_price, max_price)
        return redirect(url_for('products'))

    products, total_pages = get_paginated_products(page, page_size, search_query)

    # 计算页码显示范围
    start = max(1, page - 2)
    end = min(total_pages, page + 2)
    page_range = range(start, end + 1)

    return render_template('products.html', products=products, page=page, total_pages=total_pages,
                           search_query=search_query, page_range=page_range)


def get_paginated_products(page, page_size, search_query):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            offset = (page - 1) * page_size
            cursor.execute("SELECT product, release_date, min_price, avg_price, max_price FROM product_prices WHERE product LIKE %s LIMIT %s OFFSET %s", ('%' + search_query + '%', page_size, offset))
            products = cursor.fetchall()
            cursor.execute("SELECT COUNT(*) FROM product_prices WHERE product LIKE %s", ('%' + search_query + '%',))
            total_records = cursor.fetchone()[0]
            total_pages = (total_records + page_size - 1) // page_size
            return [{'product': p[0], 'release_date': p[1], 'min_price': p[2], 'avg_price': p[3], 'max_price': p[4]} for p in products], total_pages
    finally:
        connection.close()
def add_product(product, release_date, min_price, avg_price, max_price):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO product_prices (product, release_date, min_price, avg_price, max_price) VALUES (%s, %s, %s, %s, %s)",
                           (product, release_date, min_price, avg_price, max_price))
            connection.commit()
    finally:
        connection.close()

def update_product(product, release_date, min_price, avg_price, max_price):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE product_prices SET release_date=%s, min_price=%s, avg_price=%s, max_price=%s WHERE product=%s",
                           (release_date, min_price, avg_price, max_price, product))
            connection.commit()
    finally:
        connection.close()
@app.route('/delete_product', methods=['POST'])
def delete_product():
    release_date = request.form['release_date']
    # 假设有一个函数 delete_product_by_date() 来处理数据库删除操作
    delete_product_by_date(release_date)
    return redirect(url_for('products'))
def delete_product_by_date(release_date):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # SQL 删除语句
            sql = "DELETE FROM product_prices WHERE release_date = %s"
            cursor.execute(sql, (release_date,))
            # 提交事务
            connection.commit()
    finally:
        connection.close()

def get_all_products():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT product, release_date, min_price, avg_price, max_price FROM product_prices")
            products = cursor.fetchall()
            return [{'product': p[0], 'release_date': p[1], 'min_price': p[2], 'avg_price': p[3], 'max_price': p[4]} for p in products]
    finally:
        connection.close()
@app.route('/product_error')
def product_error():
    return render_template('error.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=39010)



