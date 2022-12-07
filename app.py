import os
import sqlite3

from flask import Flask, g, render_template, request

app = Flask(__name__)

DEBUG = os.environ.get("DEBUG")

# db setting
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("db.sqlite")
    return g.db


@app.route('/')
def index():

    db = get_db()

    cursor = db.execute("select * from データリスト order by コード")
    data = cursor.fetchall()
    db.close()

    name = "You"
    title = "Hello from app"
    response = render_template(
        "index.html",
        title=title,
        name=name,
        data=data)
    return response


@app.route('/urlparam/<data>')
def urlparam(data=None):
    response = render_template(
        "index.html",
        data=data,
    )
    return response


@app.route('/post/',methods=["POST"])
def post():
    user_id = request.form["userid"]
    post_data = request.form["text"]

    db = get_db()
    cursor = db.execute("select MAX(コード) AS max_code from データリスト")
    for row in cursor:
        new_code = row[0] + 1
    cursor.close()

    sql = "INSERT INTO データリスト(コード, テキスト, 値) values ({}, '{}', {})".format(new_code, post_data, 100)
    db.execute(sql)
    db.commit()

    cursor = db.execute("select * from データリスト order by コード")
    data = cursor.fetchall()
    db.close()

    response = render_template(
        "index.html",
        name=user_id,
        data=data,
    )
    return response


@app.route('/form/')
def form():
    db = get_db()

    response = render_template(
        "form.html",
    )
    return response

@app.route('/init_table/')
def init_table():
    db = get_db()
    # テーブル作成
    db.execute("CREATE TABLE データリスト(コード INTEGER PRIMARY KEY, テキスト STRING, 値 INTEGER)")
    # テーブルにデータを追加
    db.execute("""INSERT INTO データリスト(コード, テキスト, 値)
        values(0, 'SQLiteのテストデータ1', 100),
        values(1, 'SQLiteのテストデータ2', 200),
        values(2, 'SQLiteのテストデータ3', 300),
        values(3, 'SQLiteのテストデータ4', 400),
        """)
    db.commit()

    return render_template("index.html")


@app.route('/drop_table/')
def drop_table():
    db = get_db()
    # テーブル作成
    db.execute("DROP TABLE データリスト")

    return render_template("index.html")

if __name__ == "__main__":
    if DEBUG:
        app.run(debug=True)
