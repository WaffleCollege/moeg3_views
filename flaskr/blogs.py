from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import db

# models.pyのBlogクラスをインポート
from flaskr.models import Blog

blog_bp = Blueprint('blogs', __name__, url_prefix='/blogs')

# # ルーティング
# # /blogs にHTTPメソッドがGETでアクセスしたblogs関数を実行する
# @blog_bp.route("/blogs")
# def blogs():
#     from flask import render_template
#     # Blogテーブルから全てのデータを取得し、作成日時の降順で並び替え
#     blogs = Blog.query.order_by(Blog.created_at.desc()).all()

#     # テンプレートにblogs変数を渡す
#     return render_template('blogs.html', blogs = blogs)

# 一覧表示
@blog_bp.route('/')
def index():
    blogs = Blog.query.order_by(Blog.created_at.desc()).all()
    return render_template('blogs/index.html', blogs=blogs)

# # 新規投稿フォーム表示と投稿処理
# @blog_bp.route('/new', methods=['GET'])
# def create():
#     # blogs/new.htmlをテンプレートとしてHTMLを組み立てる
#     return render_template('blogs/new.html')

# 新規投稿フォーム表示と投稿処理
@blog_bp.route('/new', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        user_name = request.form['user_name']

        # Blogインスタンスを作成
        new_blog = Blog(title=title, body=body, user_name=user_name)
        # バリデーションを実行
        errors = new_blog.validate()

        # エラーがあればフォームに戻す
        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('blogs/new.html', title=title, body=body, user_name=user_name)
        # DBへ保存
        db.session.add(new_blog)
        db.session.commit()

# 詳細ページ URLの末尾にidがつく
@blog_bp.route('/<int:blog_id>')
def detail(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    return render_template('blogs/detail.html', blog=blog)