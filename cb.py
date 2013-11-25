"""
Crawler Benchmark


"""
# -*- coding: utf-8 -*-

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify

import logging, logging.config, yaml
logging.config.dictConfig(yaml.load(open('logging.conf')))
logFile = logging.getLogger('file')
logConsole = logging.getLogger('console')

# create our little application :)
app = Flask(__name__)

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
        # TODO: Change SQL script to don't drop the data table and transfer the configurations in it.
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
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
    modes = [{
        'name': 'Blog',
        'url': url_for('blog'),
        'enabled': True
    },
    {
        'name': 'Forum',
        'url': url_for('forum'),
        'enabled': True
    },
    {
        'name': 'Newsfeed',
        'url': url_for('newsfeed'),
        'enabled': True
    },
    {
        'name': 'Forms',
        'url': url_for('forms'),
        'enabled': True
    },
    {
        'name': 'Catalog',
        'url': url_for('catalog'),
        'enabled': True
    }]
    return render_template('index.html', modes=modes, title='Page selection')


@app.route('/blog')
def blog():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('blog.html', entries=entries, title='Blog')


@app.route('/catalog')
def catalog():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('catalog.html', entries=entries, title='Catalog')


@app.route('/newsfeed')
def newsfeed():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('newsfeed.html', entries=entries, title='Newsfeed')


@app.route('/forms')
def forms():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('forms.html', entries=entries, title='Forms')


@app.route('/forum')
def forum():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('forum.html', entries=entries, title='Forum')


@app.route('/admin')
def admin():
    flash('Welcome to the administration page')
    return render_template("admin.html", title='Admin')


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


@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404 Not Found'), 404


#@app.before_request
#def before_request():
#    strToLog = '{0} - "{1}"'.format(request.method, request.path)
#    logFile.debug(strToLog)
#    #logConsole.debug(strToLog)

@app.after_request
def per_request_callbacks(response):
    for func in getattr(g, 'call_after_request', ()):
        response = func(response)
    strToLog = '{0} - "{1}" - {2} - {3}'.format(request.method, request.path, request.routing_exception, request.environ['HTTP_USER_AGENT'])
    logFile.debug(strToLog)
    return response

if __name__ == '__main__':
    init_db()
    app.run()