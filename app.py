import csv
import math

from flask import Flask, render_template, request, redirect
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    db='bnb',
    charset='utf8'
)
cursor = conn.cursor()

app = Flask(__name__)
app.static_folder = 'static'  # 静态文件目录为 "static"
path = 'templates/'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print('用户名和密码:', username, password)
        select_sql = 'select password from user where username = %s'
        cursor.execute(select_sql, username)
        exit_password = cursor.fetchone()  # 返回的是元组
        print('exit_password:', exit_password)
        if exit_password is None or exit_password[0] != password:
            return 'password error'
        else:
            return 'login success'
    else:
        return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print('请求')
    else:
        print('显示')
        return render_template('index.html')


@app.route('/bnb', methods=['GET', 'POST'])
def bnb():
    if request.method == 'POST':
        print('请求')
    else:
        print('显示')
        page = request.args.get('page', 1, type=int)
        page_size = 12
        select_data_sql = 'SELECT id, city, name, score, hx, cz_type, kz, price, img_url FROM bnb_data ORDER BY id asc'
        cursor.execute(select_data_sql)
        total_count = cursor.rowcount
        total_page = math.ceil(total_count / page_size)
        page = max(1, min(page, total_page))
        offset = (page - 1) * page_size
        select_page_data_sql = f'{select_data_sql} LIMIT {offset}, {page_size}'
        cursor.execute(select_page_data_sql)
        datas = cursor.fetchall()
        d = {'beijing': '北京', 'shanghai': '上海'}
        return render_template('bnb.html', datas=datas, page=page, total_page=total_page, d=d)


@app.route('/rank', methods=['GET', 'POST'])
def rank():
    if request.method == 'POST':
        print('请求')
    else:
        print('显示')
        datas=[]
        with open('spider/rank_2024_07_09.csv', 'r', encoding="utf-8-sig") as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                datas.append(row)
        datas=datas[1:]
        return render_template('rank.html', datas=datas)


@app.route('/test')
def test():
    if request.method == 'POST':
        print('请求')
    else:
        print('显示')
        page = request.args.get('page', 1, type=int)
        page_size = 12
        select_data_sql = 'SELECT id, city, name, score, hx, cz_type, kz, price, img_url FROM bnb_data ORDER BY id asc'
        cursor.execute(select_data_sql)
        total_count = cursor.rowcount
        total_page = math.ceil(total_count / page_size)
        page = max(1, min(page, total_page))
        offset = (page - 1) * page_size
        select_page_data_sql = f'{select_data_sql} LIMIT {offset}, {page_size}'
        cursor.execute(select_page_data_sql)
        datas = cursor.fetchall()
        d = {'beijing': '北京', 'shanghai': '上海'}
        return render_template('test.html', datas=datas, page=page, total_page=total_page, d=d)


@app.errorhandler(404)
def catch_404(error):
    return redirect('/404')


@app.route('/404')
def notFound():
    return render_template('404.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5020, debug=True)
