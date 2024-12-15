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

    conn = get_db_connection()
    cursor = conn.cursor()

    # 일정 데이터 삽입
    cursor.execute("""
        INSERT INTO schedules (username, title, description, start_time, end_time)
        VALUES (?, ?, ?, ?, ?)
    """, (username, title, description, start_time, end_time))
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

# 일정 목록 페이지
@schedule_bp.route('/schedule/')
def schedule():
    if 'username' not in session:
        return redirect('/account/')

    username = session['username']
    conn = get_db_connection()
    cursor = conn.cursor()

    # 사용자의 일정 목록 
    cursor.execute("SELECT * FROM schedules WHERE username = ?", (username,))
    schedules = cursor.fetchall()
    conn.close()

    return render_template('schedule.html', username=username, schedules=schedules)
