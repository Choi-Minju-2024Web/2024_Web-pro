from flask import Flask, render_template, request, redirect, session, Blueprint
import sqlite3

# Blueprint 객체 생성
dashboard_bp = Blueprint('dashboard', __name__)

# 데이터베이스 연결 함수
def get_db_connection():
    conn = sqlite3.connect('Table1.db')
    conn.row_factory = sqlite3.Row
    return conn

# view_dashboard
@dashboard_bp.route('/dashboard/')
def dashboard():
    if 'username' not in session:
        return redirect('/account/')
    
    conn =get_db_connection()
    cursor = conn.cursor()

    # 현재 사용자 데이터 가져오기
    cursor.execute("SELECT * FROM user WHERE username = ?", (session['username'],))
    user_data = cursor.fetchone()

    # 게시판 데이터 가져오기
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()

    conn.close()
    return render_template('dashboard.html', user= user_data,username=session['username'], posts = posts)

 # 게시글 작성
@dashboard_bp.route('/create_post/', methods=['GET', 'POST'])
def create_post():
    if 'username' not in session:
        return redirect('/account/')

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tags = request.form['tags']

        conn = sqlite3.connect('Table1.db')
        cursor = conn.cursor()

        # 데이터베이스에 게시글 추가
        cursor.execute('''INSERT INTO posts (title, content, tags,username) VALUES (?, ?, ?, ?)''', 
                           (title, content, tags,session['username']))
        conn.commit()

        # 게시글 ID를 얻고, 해당 게시글로 리디렉션
        post_id = cursor.lastrowid
        conn.close()

        return redirect(f'/post/{post_id}')

    return render_template('create_post.html')
    
# 게시글 상세 페이지
@dashboard_bp.route('/post/<int:post_id>')
def view_post(post_id):
    if 'username' not in session:
        return redirect('/account/')
    
    conn = sqlite3.connect('Table1.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 게시글 데이터 가져오기
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()

    conn.close()

    if not post:
        return "게시글을 찾을 수 없습니다.", 404

    return render_template('view_post.html', post=post)

# 게시글 삭제 
@dashboard_bp.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    if 'username' not in session:
        return redirect('/account/')

    conn = get_db_connection()
    cursor = conn.cursor()

    # 게시글 정보 가져오기
    cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    post = cursor.fetchone()

    if post and post['username'] == session['username']:  # 게시글이 존재하고, 작성자가 현재 로그인한 사용자와 동일한 경우
        # 게시글 삭제
        cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        conn.commit()

    conn.close()

    # 게시글 삭제 후 게시판 페이지로 리디렉션
    return redirect('/dashboard/')

# 게시글 수정정
@dashboard_bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'username' not in session:
        return redirect('/account/')

    conn = sqlite3.connect('Table1.db')
    cursor = conn.cursor()

    # 게시글 가져오기
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()

    if not post:
        return "게시글이 존재하지 않습니다.", 404

    # 수정 처리
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        new_tags = request.form['tags']

        cursor.execute('''
            UPDATE posts 
            SET title = ?, content = ?, tags = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?''',
            (new_title, new_content, new_tags, post_id)
        )
        conn.commit()
        conn.close()

        return redirect('/dashboard/')

    conn.close()
    return render_template('edit_post.html', post=post)

# 태그 검색
@dashboard_bp.route('/search', methods=['GET'])
def search_posts():
    if 'username' not in session:
        return redirect('/account/')

    # 사용자가 입력한 태그를 가져옴
    tag = request.args.get('tag', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    # 태그가 포함된 게시글 검색
    cursor.execute("SELECT * FROM posts WHERE tags LIKE ?", (f'%{tag}%',))
    posts = cursor.fetchall()

    conn.close()

    # 검색 결과를 게시판 페이지에 표시
    return render_template('dashboard.html', posts=posts, tag=tag)
