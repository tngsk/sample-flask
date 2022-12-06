import os

import pymysql
from flask import Flask, render_template

app = Flask(__name__)

DEBUG = os.environ.get("DEBUG")

# db setting

db = None

if DEBUG:
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='root',
        db='testdb',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor,
    )

# db access

# cur = db.cursor()
# sql = "select * from members"
# cur.execute(sql)
# members = cur.fetchall()

# cur.close()
# db.close()

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
