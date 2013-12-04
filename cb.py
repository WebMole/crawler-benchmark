"""
Crawler Benchmark


"""
# -*- coding: utf-8 -*-

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from Pagination import Pagination


# create our little application :)
app = Flask(__name__)

PER_PAGE = 20
modes = [
    {
        'name': 'Blog',
        'route': 'blog',
        'add': 'admin/blog/add',
        'enabled': True
     },
     {
        'name': 'Forum',
        'route': 'forum',
        'add': 'admin/forum/add',
        'enabled': True
    },
    {
        'name': 'Newsfeed',
        'route': 'newsfeed',
        'add': 'admin/newsfeed/add',
        'enabled': True
    },
    {
        'name': 'Forms',
        'route': 'forms',
        'add': 'admin/forms/add',
        'enabled': True
    },
    {
        'name': 'Catalog',
        'route': 'catalog',
        'add': 'admin/catalog/add',
        'enabled': True
    }
]

def get_specific_item(table, key, value):
    for item in table:
        if item.get(key) == value:
            return item
    raise ValueError('No item found for ' + key + ":" + value)


# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE='./db/main.db',
    DEBUG=True,
    SECRET_KEY='ls20f48g578hbmflgdi3',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        for mode in modes:
            request = "drop table if exists " + mode.get("route") + ";" \
                      "    create table " + mode.get("route") + " (" \
                      "    id integer primary key autoincrement," \
                      "    title text not null," \
                      "    text text not null" \
                      ");"
            db.cursor().executescript(request)
            db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    return render_template('index.html', modes=modes, title='Page selection')


@app.route('/admin')
def admin():
    flash('Welcome to the administration page')
    return render_template("admin.html", modes=modes, title='Admin')


@app.route('/admin/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('admin'))


@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('admin'))
    return render_template('login.html', error=error)


@app.route("/modes/<type>")
def entries(type):
    try:
        mode = get_specific_item(modes, "route", type)
    except ValueError:
        return "invalid page"

    if not mode.get('enabled'):
        return "This mode is disabled"

    db = get_db()
    cur = db.execute('select title, text from ' + type + ' order by id desc')
    entries = cur.fetchall()

    return render_template('modes/' + type + '.html', entries=entries, title=type.title())


@app.route('/test/', defaults={'page': 1})
@app.route('/test/page/<int:page>')
def show_users(page):
    count = 65
    users = ["user" + str(x) for x in range(0, count)]
    if not users and page != 1:
        abort(404)
    pagination = Pagination(page, PER_PAGE, count)
    visible_users = users[(pagination.page - 1) * PER_PAGE : pagination.page * PER_PAGE]
    return render_template('test_pagination.html',
        pagination=pagination,
        users=visible_users
    )


@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404 Not Found'), 404


def url_for_other_page(page):
    """url_for helper function for pagination"""
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


if __name__ == '__main__':
    init_db()
    app.run()
