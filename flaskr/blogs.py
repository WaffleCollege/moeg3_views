from flask import Blueprint, render_template
from flaskr.db import query_db

blog_bp = Blueprint("blog", __name__)

# ルーティング
# /blogs にHTTPメソッドがGETでアクセスしたblogs関数を実行する
@blog_bp.route("/blogs")
def blogs():
   # SQLを使ってデータベースからデータを引き出す（配列の配列の形で帰ってくる）
    blogs = query_db("SELECT * FROM blogs")

    # テンプレートにblogs変数を渡す
    return render_template('blogs.html', blogs = blogs)