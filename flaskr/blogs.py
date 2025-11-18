from flask import Blueprint, render_template, request, redirect, url_for, flash
from flaskr import db
# models.pyのBlog,Commentクラスをインポート
from flaskr.models import Blog, Comment

blog_bp = Blueprint('blogs', __name__, url_prefix='/blogs')

# 一覧表示
@blog_bp.route('/')
def index():
    blogs = Blog.query.order_by(Blog.created_at.desc()).all()
    return render_template('blogs/index.html', blogs=blogs)

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

        # 保存後、詳細ページへリダイレクト
        return redirect(url_for('blogs.detail', blog_id=new_blog.id))

    # blogs/new.htmlをテンプレートとしてHTMLを組み立てる
    return render_template('blogs/new.html')

# 詳細ページ
@blog_bp.route('/<int:blog_id>')
def detail(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    return render_template('blogs/detail.html', blog=blog)

@blog_bp.route('/<int:blog_id>/edit', methods=['GET', 'POST'])
def edit(blog_id):
    # blog_idに対応するブログを取得
    blog = Blog.query.get_or_404(blog_id)

    # 更新処理
    if request.method == 'POST':
        # フォームからデータを取得してブログオブジェクトを更新
        blog.title = request.form.get('title')
        blog.body = request.form.get('body')
        blog.user_name = request.form.get('user_name')

        # バリデーションを実行
        errors = blog.validate()
        # エラーがあればフォームに戻す
        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('blogs/edit.html', blog=blog)

        # DBへ保存
        db.session.commit()
        flash('投稿を更新しました！', 'success')
        # 詳細ページへリダイレクト
        return redirect(url_for('blogs.detail', blog_id=blog.id))

    return render_template('blogs/edit.html', blog=blog)


# 削除機能
# /<blog_id>/delete にPOSTリクエストが来たら削除を実行
@blog_bp.route('/<int:blog_id>/delete', methods=['POST'])
def delete(blog_id):
    # blog_idに対応するブログを取得
    blog = Blog.query.get_or_404(blog_id)
    # ブログを削除
    db.session.delete(blog)
    db.session.commit()
    flash('投稿を削除しました。', 'success')
    # 一覧ページへリダイレクト
    return redirect(url_for('blogs.index'))

# コメント追加機能
@blog_bp.route('/<int:blog_id>/comments', methods=['POST'])
def add_comment(blog_id):
    # blog_idに対応するブログを取得
    blog = Blog.query.get_or_404(blog_id)

    # フォームからデータを取得
    body = request.form.get("body")
    user_name = request.form.get("user_name")

    # 必須チェック
    if not body or not user_name:
        flash("コメント本文と名前は必須です。", "error")
        return redirect(url_for('blogs.detail', blog_id=blog_id))

    # コメントを作成してDBに保存
    comment = Comment(body=body, user_name=user_name, blog=blog)
    db.session.add(comment)
    db.session.commit()

    flash("コメントを追加しました！")
    return redirect(url_for('blogs.detail', blog_id=blog_id))