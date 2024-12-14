from flask import Blueprint, render_template, request, redirect, session
# flask 프레임워크를 가져오고, 템플릿 렌더링, 클라이언트 요청 처리
# 사용자 다른 URL로 연결
import sqlite3 #SQLite 데이터베이스를 사용하기 위함

# Blueprint 객체 생성
connect_bp = Blueprint('connect', __name__)

@connect_bp.route('/connect/',methods=['GET'])
def connect():
   if 'username' not in session:
      return redirect('account')
   
   username = session['username']

   db = sqlite3.connect('Table1.db')
   cursor = db.cursor()
   cursor.execute("SELECT * FROM user WHERE username = ?",(username,))
   connect_user = cursor.fetchone()
   db.close()
   if connect_user:
       return render_template('contact.html', user=connect_user)
   return "사용자를 찾을 수 없습니다."