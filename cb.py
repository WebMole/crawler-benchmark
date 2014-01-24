"""
Crawler Benchmark


"""
# -*- coding: utf-8 -*-

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import logging
import logging.config
import yaml
import pygal
import re
import datetime
import json

from loremipsum import get_paragraphs, get_sentences

from Pagination import Pagination
from LoggingRequest import LoggingRequest

logging.config.dictConfig(yaml.load(open('logging.conf')))
logFile = logging.getLogger('file')
logConsole = logging.getLogger('console')

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
            # TODO: stop dropping tables and give a function to the admin to
            # reset db
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
    # todo: fix this or get count correctly cuz I'm still a noob ;)
    db = get_db()
    for mode in modes:
        cur = db.execute('select count(*) from ' + mode.get("route"))
        count = cur.fetchall()
        mode.__setitem__("count", count)

    return render_template("admin/admin.html", modes=modes, title='Admin')


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


@app.route("/admin/add/<type>", methods=['POST'])
def entries_add(type):
    if not session.get('logged_in'):
        abort(401)

    try:
        mode = get_specific_item(modes, "route", type)
    except ValueError:
        return "invalid page"

    db = get_db()
    db.execute('insert into ' + type + ' (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New ' + type + ' entry was successfully posted')
    return redirect(url_for('admin'))

# todo: Add this to the admin interface.
@app.route("/admin/add/<type>/<int:num>", methods=['POST'])
def entries_add_auto(type, num):
    if not session.get('logged_in'):
        abort(401)
        
    try:
        mode = get_specific_item(modes, "route", type)
    except ValueError:
        return "invalid page"

    #titles = get_sentences(num, False)
    #texts = get_paragraphs(num, False)
    db = get_db()
    for i in range(0, num):
        db.execute('insert into ' + type + ' (title, text) values (?, ?)', [get_sentences(1, False)[0], get_paragraphs(1, False)[0]])
    db.commit()
    flash('New automatic %d %s entrie%s successfully posted' % (num, type, 's were' if (num > 1) else ' was'))
    return redirect(url_for('admin'))

@app.route("/modes/<type>/", defaults={'page': 1})
@app.route("/modes/<type>/page/<int:page>")
def entries(type, page):
    try:
        mode = get_specific_item(modes, "route", type)
    except ValueError:
        return "invalid page"

    if not mode.get('enabled'):
        return "This mode is disabled"

    db = get_db()
    cur = db.execute('select title, text from ' + type + ' order by id desc')
    entries = cur.fetchall()

    if not entries and page != 1:
        abort(404)

    pagination = Pagination(page, PER_PAGE, len(entries))
    visible_entries = entries[
        (pagination.page - 1) * PER_PAGE: pagination.page * PER_PAGE]

    return render_template('modes/' + type + '.html',
                           pagination=pagination,
                           entries=visible_entries,
                           title=type.title()
                           )


@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/admin/results')
def results():
    from pygal.style import LightStyle
    line_chart = pygal.Line(style=LightStyle, disable_xml_declaration=True)
    line_chart.title = 'Navigation time from First request to last request'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    #line_chart.render()
    return render_template("admin/results.html", graphs = [line_chart.render()])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404 Not Found'), 404


def url_for_other_page(page):
    """url_for helper function for pagination"""
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


#@app.before_request
# def before_request():
#    strToLog = '{0} - "{1}"'.format(request.method, request.path)
#    logFile.debug(strToLog)
# logConsole.debug(strToLog)

@app.after_request
def per_request_callbacks(response):
    if not re.match(r'/admin(.*)', request.path, re.M | re.I):
        for func in getattr(g, 'call_after_request', ()):
            response = func(response)
        #strToLog = '{0} - {1} - {2} - ' \
        #           '{3} - {4} - {5}'.format(request.method,       request.path,              request.args.lists(),
        #                                    request.form.lists(), request.routing_exception, request.environ['HTTP_USER_AGENT'])
        #strToLog = '{0}\n{1}\n{2}'.format(response.__dict__, request.__dict__, session.__dict__)
        lr = LoggingRequest(
            datetime.datetime.today(
            ),  request.method,  request.path,   request.args.lists(),
            request.form.lists(),       None if (
                request.routing_exception is None) else str(
                request.routing_exception),
            request.environ['HTTP_USER_AGENT'])
        strToLog = lr.__dict__
        #strToLog = json.dumps(lr)
        logFile.debug(strToLog)
    return response

if __name__ == '__main__':
    init_db()
    app.run()
