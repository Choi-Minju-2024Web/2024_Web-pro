from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
@app.route('/dashboard/')
def dashboard():
    if 'username' not in session:
        return redirect('/account/')
    return 
def get_db_connection():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", (session['username'],))
    user_data = cursor.fetchone()
    cursor.execute("SELECT * FROM posts")  # posts 테이블에서 모든 게시물 가져오기
    posts = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', user= user_data, posts = posts)

 # 게시글 작성
@app.route('/create_post', methods=['GET', 'POST'])
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
    
# @app.route('/post/<int:post_id>')
# def post(post_id):
#     conn = get_db_connection()
#     post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
#     conn.close()
#     return render_template('post.html', post=post)

# @app.route('/create_post', methods=('GET', 'POST'))
# def create_post():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#         tags = request.form['tags']

#         conn = get_db_connection()
#         conn.execute('INSERT INTO posts (title, content, tags) VALUES (?, ?, ?)',
#                      (title, content, tags))
#         conn.commit()
#         conn.close()

#         return redirect('/board')

#     return render_template('create_post.html')

