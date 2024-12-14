from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/board')
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

if __name__ == '__main__':
    app.run(debug=True)
