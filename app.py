import os
import sqlite3

from flask import Flask, g, render_template, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SECRET_KEY'] = 'secret_key'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(30),unique=True)

# #DBのクリエイト宣言
# db.create_all()

# #DBが空の状態(最初の1回)はtestuserを作成する
# user = User.query.filter_by(username='testuser').first()
# if user is None:
#     testuser = User(username='testuser')
#     db.session.add(testuser)
#     db.session.commit()

# admin = Admin(app)
# admin.add_view(ModelView(User, db.session))



DEBUG = os.environ.get("DEBUG")

# db setting
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("db.sqlite")
    return g.db


@app.route('/')
def index():
    # user = User.query.filter_by(username='testuser').first()
    # name = user.username
    name = "You"
    title = "Hello from app"
    response = render_template(
        "index.html",
        title=title,
        name=name)
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
    user_id = request.form["user_id"]
    post_data = request.form["post_data"]

    db = get_db()

    response = render_template(
        "index.html",
        data=post_data,
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
