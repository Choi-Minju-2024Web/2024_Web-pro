from flask import Blueprint, render_template, request, redirect, session
import sqlite3

# Blueprint 
schedule_bp = Blueprint('schedule', __name__)

def get_db_connection():
    conn = sqlite3.connect('Table1.db')
    conn.row_factory = sqlite3.Row  # 결과를 딕셔너리 형식으로 반환
    return conn

# 일정 추가
@schedule_bp.route('/schedule/add', methods=['POST'])
def add_schedule():
    if 'username' not in session:
        return redirect('/account/')

    username = session['username']
    title = request.form['title']
    description = request.form['description']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    is_shared = int(request.form.get('is_shared', 0))
    team_name = request.form.get('team_name', None) if is_shared else None

    conn = get_db_connection()
    cursor = conn.cursor()

    # 일정 데이터 삽입
    cursor.execute("""
        INSERT INTO schedules (username, title, description, start_time, end_time, is_shared, team_name)
        VALUES (?, ?, ?, ?, ?,?,?)
    """, (username, title, description, start_time, end_time, is_shared, team_name))
    conn.commit()
    conn.close()

    return redirect('/schedule/')

# 일정 삭제
@schedule_bp.route('/schedule/delete/<int:schedule_id>', methods=['GET'])
def delete_schedule(schedule_id):
    if 'username' not in session:
        return redirect('/account/')

    conn = get_db_connection()
    cursor = conn.cursor()

    # 일정 삭제
    cursor.execute("DELETE FROM schedules WHERE id = ?", (schedule_id,))
    conn.commit()
    conn.close()

    return redirect('/schedule/')

@schedule_bp.route('/schedule/')
def schedule():
    if 'username' not in session:
        return redirect('/account/')

    username = session['username']
    conn = get_db_connection()
    cursor = conn.cursor()

    # 매칭된 사용자
    cursor.execute("""SELECT DISTINCT CASE WHEN sender_username = ? THEN receiver_username ELSE sender_username END AS matched_user FROM matches WHERE (sender_username = ? OR receiver_username = ?) AND status = 'accepted'""", (username, username, username))
    matched_users = [row['matched_user'] for row in cursor.fetchall()]

    # 개인 일정
    cursor.execute("SELECT * FROM schedules WHERE username = ? AND is_shared = 0", (username,))
    personal_schedules = cursor.fetchall()
    cursor.execute("""
    SELECT DISTINCT CASE WHEN sender_username = ? THEN receiver_username ELSE sender_username END AS matched_user FROM matches WHERE (sender_username = ? OR receiver_username = ?) AND status = 'accepted'""", (username, username, username))
    matched_users = [row['matched_user'] for row in cursor.fetchall()]

# 공유 일정 가져오기 (매칭된 사용자와 관련된 일정만)
    cursor.execute("""SELECT * FROM schedules WHERE is_shared = 1 AND (username = ? OR team_name IN (SELECT team_name FROM schedules WHERE username IN ({matched_users})))""".format(matched_users=','.join(['?'] * len(matched_users))), [username] + matched_users)
    shared_schedules = cursor.fetchall()

    conn.close()
    matched_users = [{'username': user} for user in matched_users]

    return render_template(
        'schedule.html', username=username,
        personal_schedules=personal_schedules, 
        shared_schedules=shared_schedules, 
        matched_users=matched_users
    )

