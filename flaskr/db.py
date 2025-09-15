import sqlite3
from datetime import datetime

import click
from flask import current_app, g

# DBとの接続のための関数
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# DBにSQLを投げて結果を受け取る関数
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# DBとの接続を閉じる関数
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# --データベースの初期化--

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# データベースの初期化のコマンドを用意
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
# データベースの初期化のコマンドを登録する
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)