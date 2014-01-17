"""
Crawler Benchmark


"""
# -*- coding: utf-8 -*-

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import logging, logging.config, yaml
import pygal

from Pagination import Pagination

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
            # TODO: stop dropping tables and give a function to the admin to reset db
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
    #todo: fix this or get count correctly cuz I'm still a noob ;)
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
    db.execute('insert into ' + type + ' (title, text) values (?, ?)', [request.form['title'], request.form['text']])
    db.commit()
    flash('New ' + type + 'entry was successfully posted')
    return redirect(url_for('admin'))


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


# @todo: remove this and add pagination to different modes
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


@app.route('/admin/results')
def results():
    from pygal.style import LightStyle
    line_chart = pygal.Line(style=LightStyle, disable_xml_declaration=True)
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
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
#def before_request():
#    strToLog = '{0} - "{1}"'.format(request.method, request.path)
#    logFile.debug(strToLog)
#    #logConsole.debug(strToLog)


@app.after_request
def per_request_callbacks(response):
    for func in getattr(g, 'call_after_request', ()):
        response = func(response)
    strToLog = '{0} - {1} - {2} - ' \
               '{3} - {4} - {5}'.format(request.method,       request.path,              request.args.lists(),
                                        request.form.lists(), request.routing_exception, request.environ['HTTP_USER_AGENT'])
    #strToLog = '{0}\n{1}\n{2}'.format(response.__dict__, request.__dict__, session.__dict__)
    logFile.debug(strToLog)
    return response


if __name__ == '__main__':
    init_db()
    app.run()
