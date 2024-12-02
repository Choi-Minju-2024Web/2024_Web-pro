from flask import Flask, render_template, request, redirect 
# flask 프레임워크를 가져오고, 템플릿 렌더링, 클라이언트 요청 처리
# 사용자 다른 URL로 연결
import sqlite3 #SQLite 데이터베이스를 사용하기 위함

app = Flask(__name__)
@app.route('/')
@app.route('/account/', methods = ['GET','POST'])

if __name__ == '__main__':
   app.debug = True
   app.run(host = '127.0.0.1',port = 5000) #포트 5000에서 실행