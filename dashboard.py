from flask import Blueprint, render_template, request, redirect, session
import sqlite3
from dashboard import dashboard_bp

# Blueprint 객체 생성
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/board')
def dashboard():
   if 'username' not in session:
      return redirect('/account/')
   return render_template('dashboard.html',username = session['username'])

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
def board():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('board.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return render_template('post.html', post=post)

@app.route('/create_post', methods=('GET', 'POST'))
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tags = request.form['tags']

        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content, tags) VALUES (?, ?, ?)',
                     (title, content, tags))
        conn.commit()
        conn.close()

        return redirect('/board')

    return render_template('create_post.html')

