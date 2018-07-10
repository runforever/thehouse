from flask import (
    Flask,
    render_template,
    g,
)

import psycopg2

app = Flask(__name__)


@app.before_request
def get_db():
    if 'db' not in g:
        hostname = 'postgres'
        username = 'admin'
        password = 'root'
        database = 'caterpillar'
        g.db = psycopg2.connect(
            host=hostname,
            user=username,
            password=password,
            dbname=database
        )

    if 'cursor' not in g:
        g.cursor = g.db.cursor()


@app.teardown_request
def close_db(e=None):
    cursor = g.pop('cursor', None)
    if cursor is not None:
        cursor.close()

    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route("/")
def hello():
    g.cursor.execute("""SELECT id from house""")
    rows = g.cursor.fetchall()
    for r in rows:
        print(r)
    return render_template('index.html')
