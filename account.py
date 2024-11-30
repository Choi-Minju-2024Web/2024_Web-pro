from flask import Flask, render_template,request,redirect
import sqlite3

app = Flask(__name__)

@app.route('/account/', methods=['GET', 'POST'])