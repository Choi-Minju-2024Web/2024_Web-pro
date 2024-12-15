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

@match_bp.route('/connect/',methods=['GET'])
def connect():
   if 'username' not in session:
      return redirect('/account/')
   
   username = session['username']

   db = sqlite3.connect('Table1.db')
   cursor = db.cursor()
   # 받은 매칭 요청
   cursor.execute("SELECT id, sender_username FROM matches WHERE receiver_username = ? AND status IS 'pending'",(username,),)
   received_requests = cursor.fetchall()

    # 매칭된 유저
   cursor.execute(
        "SELECT receiver_username FROM matches WHERE sender_username = ? AND status = 'accepted' ""UNION ""SELECT sender_username FROM matches WHERE receiver_username = ? AND status = 'accepted'",(username, username),)
   confirmed_matches = [row[0] for row in cursor.fetchall()]
   db.close()

   return render_template('connect.html', received_requests=received_requests,  confirmed_matches=confirmed_matches)

@match_bp.route('/send_request/<string:receiver_username>', methods=['GET'])
def send_request(receiver_username):
    if 'username' not in session:
        return redirect('/account/')

    sender_username = session['username']

    conn = sqlite3.connect('Table1.db')
    cursor = conn.cursor()

    try:
        # 이미 요청을 보낸 적이 있는지 확인 (상태가 'pending'인 요청이 있는지)
        cursor.execute("""
            SELECT * FROM matches 
            WHERE sender_username = ? AND receiver_username = ? AND status = 'pending'
        """, (sender_username, receiver_username))
        existing_request = cursor.fetchone()

        if existing_request:
            return '', 204  # 이미 요청을 보낸 경우, 상태 코드 204로 이미 요청을 보낸 경우를 처리
        
        # 요청이 없다면 새로운 매칭 요청을 'pending' 상태로 DB에 추가
        cursor.execute("""
            INSERT INTO matches (sender_username, receiver_username, status) 
            VALUES (?, ?, 'pending')
        """, (sender_username, receiver_username))
        conn.commit()

    except sqlite3.OperationalError as e:
        print("SQLite OperationalError:", e)
        return '', 500  # 오류 발생 시, 500 상태 코드 반환

    finally:
        conn.close()

    return '', 204  # 요청 성공 시, 빈 응답과 함께 상태 코드 204 반환

@match_bp.route('/accept_request/<int:request_id>', methods=['GET'])
def accept_request(request_id):
    conn = sqlite3.connect('Table1.db')
    conn.execute('PRAGMA busy_timeout = 3000')  # 3초 동안 잠금을 기다림
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT sender_username, receiver_username FROM matches WHERE id = ?", (request_id,))
        request_data = cursor.fetchone()

        if request_data:
            sender_username, receiver_username = request_data

            # 이미 'accepted' 상태인 매칭이 있는지 확인 / 중복 방지
            cursor.execute("SELECT * FROM matches WHERE sender_username = ? AND receiver_username = ? AND status = 'accepted'", 
                           (sender_username, receiver_username))
            existing_match = cursor.fetchone()

            if not existing_match:
                # 매칭을 수락, 기존 'pending' 요청을 'accepted'로 변경
                cursor.execute("UPDATE matches SET status = 'accepted' WHERE id = ?", (request_id,))
                conn.commit()
            else:
                # 이미 매칭이 존재하는 경우
                print("Error: Duplicate match exists")
        else:
            # request_id가 유효하지 않거나 해당 요청이 없는 경우
            print("Error: Request ID not found")
    except sqlite3.OperationalError as e:
        print("SQLite OperationalError:", e)
    finally:
        conn.close()

    return redirect('/connect/')

@match_bp.route('/reject_request/<int:request_id>', methods=['GET'])
def reject_request(request_id):
    conn = sqlite3.connect('Table1.db')
    conn.execute('PRAGMA busy_timeout = 3000')  # 3초 동안 잠금기다리기
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT sender_username, receiver_username FROM matches WHERE id = ?", (request_id,))
        request_data = cursor.fetchone()

        if request_data:
            # 요청을 거절, status를 'rejected'로 변경
            cursor.execute("DELETE FROM matches WHERE id = ?", (request_id,))
            conn.commit()
        else:
            # request_id가 유효하지 않거나 해당 요청이 없는 경우
            print("Error: Request ID not found")
    except sqlite3.OperationalError as e:
        print("SQLite OperationalError:", e)
    finally:
        conn.close() 

    return redirect('/connect/')

@match_bp.route('/disconnect_match/<string:username>', methods=['GET'])
def disconnect_match(username):
    conn = sqlite3.connect('Table1.db')
    cursor = conn.cursor()
    current_user = session['username']

    try:
        # 매칭된 유저 삭제 
        cursor.execute("""DELETE FROM matches WHERE (sender_username = ? AND receiver_username = ?) OR (sender_username = ? AND receiver_username = ?)""", (current_user, username, username, current_user))
        conn.commit()
    except sqlite3.OperationalError as e:
        print("SQLite OperationalError:", e)
    finally:
        conn.close()

    return redirect('/connect/') 
