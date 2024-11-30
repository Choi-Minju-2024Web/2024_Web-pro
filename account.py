from flask import Flask, render_template,request,redirect
import sqlite3

app = Flask(__name__)
@app.route('/account/', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
       db = sqlite3.connect('Table1.db')
       username = request.form['username']
       password = request.form['password']
       conn = sqlite3.connect('user.db') #데이터 베이스 연결하고 저장
       cursor = conn.cursor()
       
if __name__ == '_main_':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)