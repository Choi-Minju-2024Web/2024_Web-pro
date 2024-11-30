from flask import Flask, render_template,request,redirect
import sqlite3

app = Flask(__name__)
@app.route('/')
@app.route('/account/', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
       db = sqlite3.connect('Table1.db')
       cursor = db.cursor()
       username = request.form['username']
       password = request.form['password'] #데이터 베이스 연결하고 저장
       try:
           cursor.execute('INSERT INTO user (username,password) VALUES (?, ?)', (username, password))
           db.commit()
       except sqlite3.IntegrityError:
           return "유저 이미 존재"
       db.close()
       return redirect('/account/')
    return render_template('account.html')
        
if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)