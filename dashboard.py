from flask import Blueprint, render_template, request, redirect, session
import sqlite3

# Blueprint 객체 생성
def create_dashboard_bp():
    dashboard_bp = Blueprint('dashboard', __name__)

    @dashboard_bp.route('/dashboard/')
    def dashboard():
        if 'username' not in session:
            return redirect('/account/')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ?", (session['username'],))
        user_data = cursor.fetchone()
        cursor.execute("SELECT * FROM posts")  # posts 테이블에서 모든 게시물 가져오기
        posts = cursor.fetchall()
        conn.close()
        return render_template('dashboard.html', user= user_data, posts = posts)
    return dashboard_bp
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

