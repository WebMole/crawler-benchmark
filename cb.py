"""
Crawler Benchmark


"""
# -*- coding: utf-8 -*-
import StringIO
import random

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

import logging
import logging.config
import yaml
import re
from datetime import datetime, date
from calendar import Calendar

from loremipsum import get_paragraphs, get_sentences

from Pagination import Pagination
from LoggingRequest import LoggingRequest

from Config import Config

import GraphManager
import LogParser

logging.config.dictConfig(yaml.load(open('logging.conf')))
logFile = logging.getLogger('file')
logConsole = logging.getLogger('console')

# create our little application :)
app = Flask(__name__)


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
config = Config


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()

        for mode in config.modes:
            # create tables if not already created
            request = "    create table if not exists " + mode.get("route") + " (" \
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
    return render_template('index.html', modes=config.modes, title='Page selection')


@app.route('/admin')
def admin():
    db = get_db()
    for mode in config.modes:
        cur = db.execute('select count(id) from ' + mode.get("route"))
        count = cur.fetchone()
        mode.__setitem__('count', count[0])

    return render_template("admin/admin.html", modes=config.modes, title='Admin')


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


@app.route("/admin/add/<string:type>", methods=['POST'])
def entries_add(type):
    if not session.get('logged_in'):
        abort(401)

    try:
        mode = get_specific_item(config.modes, "route", type)
    except ValueError:
        return "invalid page"

    db = get_db()
    db.execute('insert into ' + type + ' (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New ' + type + ' entry was successfully posted')
    return redirect(url_for('admin'))


# todo: Add this to the admin interface.


@app.route("/admin/add/<string:type>/<int:num>", methods=['POST'])
def entries_add_auto(type, num):
    if not session.get('logged_in'):
        abort(401)

    try:
        mode = get_specific_item(config.modes, "route", type)
    except ValueError:
        return "invalid page"

    db = get_db()
    for i in range(0, num):
        db.execute('insert into ' + type + ' (title, text) values (?, ?)',
                   [get_sentences(1, False)[0].replace(".", ""), get_paragraphs(1, False)[0]])
    db.commit()
    flash('New automatic %d %s entrie%s successfully posted' %
          (num, type, 's were' if (num > 1) else ' was'))
    return redirect(url_for('admin'))


@app.route("/admin/clear/<type>", methods=['DELETE'])
def clear_entries(type):
    """Creates the database tables."""
    with app.app_context():
        db = get_db()

        try:
            mode = get_specific_item(config.modes, "route", type)
        except ValueError:
            abort(404)

        request = "drop table if exists " + type + ";"
        db.cursor().executescript(request)
        db.commit()
        init_db()
        return "OK"


@app.route("/modes/<type>/", defaults={'page': 1})
@app.route("/modes/<type>/page/<int:page>")
def entries(type, page):
    try:
        mode = get_specific_item(config.modes, "route", type)
    except ValueError:
        return "invalid page"

    if not mode.get('enabled'):
        return "This mode is disabled"

    # todo: add a request to get the count and another using LIMIT <skip>, <count> or LIMIT <count> OFFSET <skip>
    db = get_db()
    cur = db.execute('select id, title, text from ' + type + ' order by id desc')
    entries = cur.fetchall()

    if not entries and page != 1:
        abort(404)

    pagination = Pagination(page, config.pagination_entry_per_page, len(entries))
    visible_entries = entries[
                      (
                          pagination.page - 1) * config.pagination_entry_per_page: pagination.page * config.pagination_entry_per_page]

    return render_template('modes/' + type + '.html',
                           pagination=pagination,
                           entries=visible_entries,
                           title=type.title(),
                           type=type,
                           config=config
    )


@app.route("/modes/<string:type>/<int:id>")
def entry(type, id):
    try:
        mode = get_specific_item(config.modes, "route", type)
    except ValueError:
        return "invalid page"

    if not mode.get('enabled'):
        return "This mode is disabled"

    db = get_db()
    cur = db.execute('select id, title, text from ' + type + ' where id = ' + str(id))
    entry = cur.fetchall()

    if not entry:
        abort(404)

    return render_template('modes/' + type + '.html',
                           entries=entry,
                           title=type.title()
    )


@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


#@app.route('/admin/plot.png')
@app.route('/admin/plot.svg')
def plot():
    from flask import make_response

    output = GraphManager.draw_custom_graph(user_agents=request.values.getlist('selUserAgent'))
    response = make_response(output.getvalue())
    #response.mimetype = 'image/png'
    response.mimetype = 'image/svg+xml'
    return response


@app.route('/admin/results')
def results():
    return render_template("admin/results.html",
                           user_agents=LogParser.get_log_user_agents()
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404 Not Found'), 404


@app.route('/trap/random/')
def trap_random_page():
    return render_template('traps/random.html',
                           title=get_sentences(1, False)[0],
                           content=get_sentences(random.randint(1, 5)),
                           config=config
    )


@app.route('/trap/login/')
def trap_login():
    return render_template('traps/login.html',
                           title=get_sentences(1, False)[0],
                           content=get_sentences(random.randint(1, 5)),
                           config=config
    )


@app.route('/trap/outgoing/')
def trap_outgoing():
    return render_template('traps/outgoing.html',
                           title=get_sentences(1, False)[0],
                           content=get_sentences(random.randint(1, 5)),
                           config=config
    )


@app.route('/trap/parameters/')
def trap_parameters():
    return render_template('traps/parameters.html',
                           title=get_sentences(1, False)[0],
                           content=get_sentences(random.randint(1, 5)),
                           config=config
    )


@app.route('/trap/session-variables/')
def trap_session_variables():
    return render_template('traps/parameters.html',
                           title=get_sentences(1, False)[0],
                           content=get_sentences(random.randint(1, 5)),
                           config=config
    )


@app.route('/trap/calendar/', defaults={'year': None})
@app.route('/trap/calendar/<int:year>/')
def trap_calendar(year):
    cal = Calendar(0)
    try:
        if year is None:
            year = date.today().year
            yearMod = year
        else:
            yearMod = year % 10000
            if yearMod < 1:
                yearMod = 1
        cal_list = [cal.monthdatescalendar(yearMod, i + 1) for i in xrange(12)]
    except Exception, e:
        abort(500)
    else:
        return render_template('traps/calendar.html', year=year, calendar=cal_list)
    abort(501)


@app.route('/trap/errors/')
def trap_errors():
    return render_template('traps/errors.html',
                           title=get_sentences(1, False)[0],
                           content=get_sentences(random.randint(1, 5)),
                           config=config
    )


@app.route('/trap/deadends/')
def trap_deadends():
    return render_template('traps/deadends.html',
                           title=get_sentences(1, False)[0],
                           content=get_sentences(random.randint(1, 5)),
                           config=config
    )


@app.route('/trap/comet/')
def trap_comet():
    return render_template('traps/comet.html',
                           title=get_sentences(1, False)[0],
                           content=get_sentences(random.randint(1, 5)),
                           config=config
    )


@app.route('/trap/depth/')
def trap_depth():
    return render_template('traps/depth.html',
                           title=get_sentences(1, False)[0],
                           content=get_sentences(random.randint(1, 5)),
                           config=config
    )


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
            datetime.today(
            ), request.method, request.path, request.args.lists(),
            request.form.lists(), None if (
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
