import psycopg2
import psycopg2.extras

from flask import (
    Flask,
    render_template,
    g,
    jsonify,
)

app = Flask(__name__)


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
            dbname=database,
        )
    return g.db


@app.teardown_appcontext
def teardown_db(e):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def iter_row(cursor, size=300):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break

        for row in rows:
            yield row


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/house')
def house():
    with get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("""SELECT id, house from house""")
        house = [row for row in iter_row(cur, 300)]

    return jsonify(house)
