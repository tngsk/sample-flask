import os
import sqlite3

from flask import Flask, g, render_template, request

app = Flask(__name__)

# -------------------------------------------------------
# db setting
# -------------------------------------------------------
def rino_get_db():
    if 'rino_db' not in g:
        g.rino_db = sqlite3.connect("rino_db.sqlite")
    return g.rino_db

# -------------------------------------------------------
# db setting
# -------------------------------------------------------
def yuki_get_db():
    if 'yuki_db' not in g:
        g.yuki_db = sqlite3.connect("yuki_db.sqlite")
    return g.yuki_db

# -------------------------------------------------------
# db setting
# -------------------------------------------------------
def nachi_get_db():
    if 'nachi_db' not in g:
        g.nachi_db = sqlite3.connect("nachi_db.sqlite")
    return g.nachi_db


# -------------------------------------------------------
# トップページ
# -------------------------------------------------------
@app.route('/rino/')
def rino_index():

    # 保存してあるデータを取り出す
    db = rino_get_db()
    cursor = db.execute("select * from 保管場所 order by コード")
    data = cursor.fetchall()
    db.close()

    # ページ内容をきめる
    return render_template("rino_index.html", memo=data[-1][1])

# -------------------------------------------------------
# トップページ
# -------------------------------------------------------
@app.route('/yuki/')
def yuki_index():

    # 保存してあるデータを取り出す
    db = yuki_get_db()
    cursor = db.execute("select * from 保管場所 order by コード")
    data = cursor.fetchall()
    db.close()

    # ページ内容をきめる
    return render_template("yuki_index.html", memo=data[-1][1])

# -------------------------------------------------------
# トップページ
# -------------------------------------------------------
@app.route('/nachi/')
def nachi_index():

    # 保存してあるデータを取り出す
    db = nachi_get_db()
    cursor = db.execute("select * from 保管場所 order by コード")
    data = cursor.fetchall()
    db.close()

    # ページ内容をきめる
    return render_template("nachi_index.html", memo=data[-1][1])


# -------------------------------------------------------
# データ登録
# -------------------------------------------------------
@app.route('/rino/save/',methods=["POST"])
def rino_save():
    data = request.form["memo"]
    hito = request.form["hito"]    
    # データベースの空き場所を探す
    db = rino_get_db()
    cursor = db.execute("select MAX(コード) AS max_code from 保管場所")
    for row in cursor:
        new_code = row[0] + 1
    cursor.close()
    
    # 空いてる場所に保管する
    sql = "INSERT INTO 保管場所(コード, メモ, 人) values ({}, '{}', '{}')".format(new_code, data, hito)
    db.execute(sql)
    db.commit()

    # とってくる
    cursor = db.execute("select * from 保管場所 order by コード")
    data = cursor.fetchall()
    db.close()

    response = render_template(
        "rino_index.html",
        memo=data[-1][1]
    )
    return response

# -------------------------------------------------------
# データ登録
# -------------------------------------------------------
@app.route('/yuki/save/',methods=["POST"])
def yuki_save():
    data = request.form["memo"]
    hito = request.form["hito"]    
    # データベースの空き場所を探す
    db = yuki_get_db()
    cursor = db.execute("select MAX(コード) AS max_code from 保管場所")
    for row in cursor:
        new_code = row[0] + 1
    cursor.close()
    
    # 空いてる場所に保管する
    sql = "INSERT INTO 保管場所(コード, メモ, 人) values ({}, '{}', '{}')".format(new_code, data, hito)
    db.execute(sql)
    db.commit()

    # とってくる
    cursor = db.execute("select * from 保管場所 order by コード")
    data = cursor.fetchall()
    db.close()

    response = render_template(
        "yuki_index.html",
        memo=data[-1][1]
    )
    return response

# -------------------------------------------------------
# データ登録
# -------------------------------------------------------
@app.route('/nachi/save/',methods=["POST"])
def nachi_save():
    data = request.form["memo"]
    hito = request.form["hito"]    
    # データベースの空き場所を探す
    db = nachi_get_db()
    cursor = db.execute("select MAX(コード) AS max_code from 保管場所")
    for row in cursor:
        new_code = row[0] + 1
    cursor.close()
    
    # 空いてる場所に保管する
    sql = "INSERT INTO 保管場所(コード, メモ, 人) values ({}, '{}', '{}')".format(new_code, data, hito)
    db.execute(sql)
    db.commit()

    # とってくる
    cursor = db.execute("select * from 保管場所 order by コード")
    data = cursor.fetchall()
    db.close()

    response = render_template(
        "nachi_index.html",
        memo=data[-1][1]
    )
    return response

# -------------------------------------------------------
# 最初にやる データベースを作る
# -------------------------------------------------------
@app.route('/init_table/')
def init_table():
    db = rino_get_db()
    # テーブル作成
    db.execute("CREATE TABLE 保管場所(コード INTEGER PRIMARY KEY, メモ STRING, 人 STRING)")
    # テーブルにデータを追加
    db.execute("""INSERT INTO 保管場所(コード, メモ, 人)
        values (0, 'これまで起きた出来事や思ったことをメモしよう', '人')
        """)
    db.commit()

    db2 = yuki_get_db()
    # テーブル作成
    db2.execute("CREATE TABLE 保管場所(コード INTEGER PRIMARY KEY, メモ STRING, 人 STRING)")
    # テーブルにデータを追加
    db2.execute("""INSERT INTO 保管場所(コード, メモ, 人)
        values (0, 'これまで起きた出来事や思ったことをメモしよう', '人')
        """)
    db2.commit()

    db3 = nachi_get_db()
    # テーブル作成
    db3.execute("CREATE TABLE 保管場所(コード INTEGER PRIMARY KEY, メモ STRING, 人 STRING)")
    # テーブルにデータを追加
    db3.execute("""INSERT INTO 保管場所(コード, メモ, 人)
        values (0, 'これまで起きた出来事や思ったことをメモしよう', '人')
        """)
    db3.commit()

    return render_template("rino_index.html")

# -------------------------------------------------------
# 絶対いる
# -------------------------------------------------------
if __name__ == "__main__":
    # if DEBUG:
    app.run(debug=True)
