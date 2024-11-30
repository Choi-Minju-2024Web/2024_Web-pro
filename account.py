from flask import Flask, render_template,request,redirect
import sqlite3

app = Flask(__name__)

@app.route('/account/', methods=['GET', 'POST'])


if __name__ == '_main_':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)