from flask import Blueprint, render_template, request, redirect, session
# flask 프레임워크를 가져오고, 템플릿 렌더링, 클라이언트 요청 처리
# 사용자 다른 URL로 연결
import sqlite3 #SQLite 데이터베이스를 사용하기 위함

# Blueprint 객체 생성
match_bp = Blueprint('match', __name__)

@match_bp.route('/match/',methods=['GET','POST'])
def match():
   if 'username' not in session:
      return redirect('account')

   if request.method == 'POST':
      role = request.form['role'] #멘토 멘티 역할 선택
      db = sqlite3.connect('Table1.db')
      cursor=db.cursor()

      #매칭 사용자 찾기
      if role == 'mentor':
         cursor.execute("SELECT * FROM user WHERE role = 'mentee'")
      elif role == 'mentee':
         cursor.execute("SELECT * FROM user WHERE role = 'mentor'")
      elif role == 'team':
         cursor.execute("SELECT * FROM user WHERE role = 'team'")
      matches = cursor.fetchall()
      db.close()

      return render_template('match_result.html', username=session['username'], matches=matches)
   return render_template('match.html',username=session['username'])