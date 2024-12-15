from flask import Flask, render_template, request, redirect, session, Blueprint
import sqlite3

# Blueprint 객체 생성
dashboard_bp = Blueprint('dashboard', __name__)

# 데이터베이스 연결 함수
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # 결과를 딕셔너리 형식으로 반환
    return conn

def create_tables():
    conn=sqlite3.connect('Table1.db')
    cursor=conn.cursor()
        # posts 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

create_tables()

def dashboard():
    if 'username' not in session:
        return redirect('/account/')
    
    conn =get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user WHERE username = ?", (session['username'],))
    user_data = cursor.fetchone()

    cursor.execute("SELECT * FROM posts")  # posts 테이블에서 모든 게시물 가져오기
    posts = cursor.fetchall()

    conn.close()
    return render_template('dashboard.html', user= user_data, posts = posts)

 # 게시글 작성
@dashboard_bp.route('/create_post/', methods=['GET', 'POST'])
def create_post():
    if 'username' not in session:
        return redirect('/account/')

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tags = request.form['tags']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # 데이터베이스에 게시글 추가
        cursor.execute('''INSERT INTO posts (title, content, tags) VALUES (?, ?, ?)''', 
                           (title, content, tags))
        conn.commit()

        # 게시글 ID를 얻고, 해당 게시글로 리디렉션
        post_id = cursor.lastrowid
        conn.close()

        return redirect(f'/post/{post_id}')

    return render_template('create_post.html')
    
# 게시글 상세 페이지
@dashboard_bp.route('/post/<int:post_id>')
def post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return render_template('post.html', post=post)
