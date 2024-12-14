from flask import Flask, render_template, request, redirect, session
# flask 프레임워크를 가져오고, 템플릿 렌더링, 클라이언트 요청 처리
# 사용자 다른 URL로 연결
import sqlite3 #SQLite 데이터베이스를 사용하기 위함

# 경로설정
app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
#로그인 시 대쉬보드로 이동
def home():
   if 'username' in session:
      return redirect('/dashboard/')
   return redirect('/account/')

@app.route('/account/', methods = ['GET','POST'])
#함수 선언
def account():
   #회원가입 데이터 저장
   #만약 POST요청이 들어오면
   if request.method == 'POST':
      #Table1.db에 연결
      db = sqlite3.connect('Table1.db')
      cursor = db.cursor()
      #html 폼에서 입력받은 값 각각 가져오기
      username = request.form['username']
      password = request.form['password']
      field = request.form.get('field')
      experience =int(request.form.get('experience'))

      #유저 저장
      try:
         cursor.execute('INSERT INTO user (username, password, field, experience) VALUES (?, ?, ?, ?)', (username, password, field, experience))
         db.commit()
         #로그인 시 세션에 username 저장하기
         session['username'] = username
      # 만약 유저이름이 중복되면 에러 메시지 반환   
      except sqlite3.IntegrityError:
         return "이미 존재하는 이름입니다."
      db.close()
      # 저장에 성공하면 다시 '/account/'로
      return redirect('/account/')
   # GET 요청일 경우 account.html 파일 반환해 이용자에게 표시
   return render_template('account.html')   

@app.route('/login/',methods = ['POST'])
def login():
   username = request.form.get('username')
   password = request.form.get('password')
   db = sqlite3.connect('Table1.db')
   cursor = db.cursor()
   cursor.execute('SELECT * FROM user WHERE username = ? AND password = ?', (username,password))
   # 가입된 유저 정보 가져오기
   user = cursor.fetchone()
   db.close()
   if user:
      #로그인 성공
      session['username']= username
      return redirect('/dashboard/')
   return "로그인 실패"

@app.route('/dashboard/')
def dashboard():
   if 'username' not in session:
      return redirect('/account/')
   return render_template('dashboard.html',username = session['username'])

@app.route('/logout/')
def logout():
   session.pop('username',None) #세션 제거하기
   return redirect('/account/')

@app.route('/match/',methods=['GET','POST'])
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

      return render_template('match_result.html',matches = matches)
   return render_template('match.html')

@app.route('/schedule/')
def schedule():
   if 'username' not in session:
      return redirect('/account/')
   return render_template('schedule.html')

if __name__ == '__main__':
   app.debug = True
   app.run(host = '127.0.0.1',port = 5000) #포트 5000에서 실행
