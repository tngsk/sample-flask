import os
import sqlite3

from flask import Flask, g, render_template

app = Flask(__name__)

DEBUG = os.environ.get("DEBUG")

# db setting
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("db.sqlite")
    return g.db

@app.route('/')
def index():
    name = "You"
    title = "Flask Test"
    response = render_template(
        "index.html",
        title=title,
        name=name)
    return response

@app.route('/post/<data>')
def post(data=None):
    response = render_template(
        "index.html",
        data=data,
    )
    return response

if __name__ == "__main__":
    if DEBUG:
        app.run(debug=True)
