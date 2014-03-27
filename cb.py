"""
Crawler Benchmark
"""
# -*- coding: utf-8 -*-
import random
import logging
import logging.config
import re
from datetime import datetime, date
from calendar import Calendar
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
import yaml
from loremipsum import get_paragraphs, get_sentences

from Pagination import Pagination
from LoggingRequest import LoggingRequest
from Config import Config
import GraphManager
import log_parser


logging.config.dictConfig(yaml.load(open('logging.conf')))
log_file = logging.getLogger('file')
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


def connect_db(database_name):
    """Connects to the specific database."""
    rv = sqlite3.connect(database_name)
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()

        for mode in config.modes:
            # create tables if not already created
            database_request = "create table if not exists " \
                               + mode.get("route") \
                               + " (" \
                                 "    id integer primary key autoincrement," \
                                 "    title text not null," \
                                 "    text text not null" \
                                 ");"
            db.cursor().executescript(database_request)
            db.commit()


def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db(app.config["DATABASE"])
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if error is not None:
        raise Exception(str(error))
    else:
        if hasattr(g, 'sqlite_db'):
            g.sqlite_db.close()
        else:
            abort(500, "Database not loaded yet")


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

    return render_template(
        "admin/admin.html",
        modes=config.modes,
        title='Admin',
        in_admin=True
    )


@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = "True"
            flash('You were logged in')
            return redirect(url_for('admin'))
    return render_template('login.html', error=error)


@app.route("/admin/add/<string:mode>", methods=['POST'])
def entries_add(mode):
    if not session.get('logged_in'):
        abort(401)

    try:
        mode = get_specific_item(config.modes, "route", mode)
    except ValueError:
        return "invalid page"

    db = get_db()
    db.execute('insert into ' + mode + ' (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New ' + mode + ' entry was successfully posted')
    return redirect(url_for('admin'))


# todo: Add this to the admin interface.
@app.route("/admin/add/<string:mode>/<int:num>", methods=['POST'])
def entries_add_auto(mode, num):
    if not session.get('logged_in'):
        abort(401)

    try:
        mode = get_specific_item(config.modes, "route", mode)
    except ValueError:
        return "invalid page"

    db = get_db()
    for i in range(0, num):
        db.execute(
            'insert into ' + mode +
            ' (title, text) values (?, ?)',
            [get_sentences(1, False)[0].replace(".", ""), get_paragraphs(1, False)[0]]
        )
    db.commit()
    flash('New automatic %d %s entrie%s successfully posted' %
          (num, mode, 's were' if (num > 1) else ' was'))
    return redirect(url_for('admin'))


@app.route("/admin/clear/<string:mode>", methods=['DELETE'])
def clear_entries(mode):
    """Creates the database tables."""
    with app.app_context():
        db = get_db()

        try:
            mode = get_specific_item(config.modes, "route", mode)
        except ValueError:
            abort(404)

        database_request = "drop table if exists " + mode + ";"
        db.cursor().executescript(database_request)
        db.commit()
        init_db()
        return "OK"


@app.route("/modes/<string:mode>/", defaults={'page_number': None})
@app.route("/modes/<string:mode>/page/<int:page_number>")
def entries(mode, page_number):
    try:
        mode = get_specific_item(config.modes, "route", mode)
    except ValueError:
        return "invalid page"

    if not mode.get('enabled'):
        return "This mode is disabled"

    pagination = None
    mode_entries = None

    # todo: Chose if ajax_enabled and infinite_scroll_enabled configs are for each separate modes or globals
    ajax_enabled = config.ajax_enabled
    infinite_scroll_enabled = config.infinite_scroll_enabled

    if ajax_enabled and page_number is None:
        no_layout = False
    else:
        if ajax_enabled:
            no_layout = True
        else:  # AJAX is disabled
            no_layout = False
            infinite_scroll_enabled = False
            if page_number is None:
                page_number = 1
        db = get_db()

        cur = db.execute('select count(id) from ' + mode.get("route"))
        count = cur.fetchone()
        count_value = count[0]

        pagination = Pagination(
            page_number,
            config.pagination_entry_per_page,
            count_value
        )

        db = get_db()
        cur = db.execute(
            'select id, title, text from %s order by id desc limit %d offset %d' % (
                mode.get('route'),
                config.pagination_entry_per_page,
                (pagination.page - 1) * config.pagination_entry_per_page
            )
        )
        mode_entries = cur.fetchall()

        if not mode_entries and page_number != 1:
            abort(404)

    return render_template(
        'modes/' + mode.get('route') + '.html',
        pagination=pagination,
        entries=mode_entries,
        title=mode.get('name'),
        mode=mode.get('route'),
        config=config,
        ajaxOn=ajax_enabled,
        infiniteScrollOn=infinite_scroll_enabled,
        noLayout=no_layout
    )


@app.route("/modes/<string:mode>/<int:mode_id>")
def entry(mode, mode_id):
    try:
        mode = get_specific_item(config.modes, "route", mode)
    except ValueError:
        return "invalid page"

    if not mode.get('enabled'):
        return "This mode is disabled"

    db = get_db()
    cur = db.execute('select id, title, text from ' + mode.get('route') + ' where id = ' + str(mode_id))
    mode_entry = cur.fetchall()

    if not mode_entry:
        abort(404)

    return render_template(
        'modes/' + mode.get('route') + '.html',
        entries=mode_entry,
        title=mode.get('name')
    )


@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


#TODO: fix the image display...
#@app.route('/admin/plot.png')
@app.route('/admin/plot.svg')
def plot():
    from flask import make_response

    output = GraphManager.draw_custom_graph(user_agents=request.values.getlist('selUserAgent'))
    response = make_response(output.getvalue())
    #response.mimetype = 'image/png'
    response.mimetype = 'image/svg+xml'
    return response


@app.route('/admin/clear_log_user_agents', methods=['DELETE'])
def clear_log_user_agents():
    log_parser.clear_log(user_agents=request.values.getlist('selUserAgent'))
    return "OK"


@app.route('/admin/results')
def results():
    return render_template(
        "admin/results.html",
        user_agents=log_parser.get_log_user_agents(),
        in_admin=True
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title=e), 404


@app.route('/trap/random/')
def trap_random_page():
    return render_template(
        'traps/random.html',
        title=get_sentences(1, False)[0],
        content=get_sentences(random.randint(1, 5)),
        config=config
    )


@app.route('/trap/login/', methods=['GET', 'POST'])
def trap_login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != "test":
            error = 'Invalid username'
        elif request.form['password'] != "test":
            error = 'Invalid password'
        else:
            session['trap_logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('success', challenge="login"))

    return render_template(
        'traps/login.html',
        title=get_sentences(1, False)[0],
        content=get_sentences(random.randint(1, 5)),
        error=error,
        config=config
    )


@app.route('/trap/outgoing/')
def trap_outgoing():
    return render_template(
        'traps/outgoing.html',
        title=get_sentences(1, False)[0],
        content=get_sentences(random.randint(1, 5)),
        config=config,
        links=config.links["external"],
        next=url_for("success", challenge="outgoing")
    )


@app.route('/trap/parameters/')
def trap_parameters():
    return render_template(
        'traps/parameters.html',
        title=get_sentences(1, False)[0],
        content=get_sentences(random.randint(1, 5)),
        config=config
    )


@app.route('/trap/cookies/')
def trap_cookies():
    resp = make_response(
        render_template(
            'traps/cookies.html',
            title=get_sentences(1, False)[0],
            content=get_sentences(random.randint(1, 5)),
            config=config
        )
    )
    resp.set_cookie('crawler_stores_cookies', 'yes')
    return resp


@app.route('/trap/cookies/verify')
def trap_cookies_verify():
    crawler_supports_cookies = request.cookies.get('crawler_stores_cookies')
    if crawler_supports_cookies == "yes":
        return redirect(url_for('success', challenge="cookies"))
    else:
        return redirect(url_for('fail', challenge="cookies"))


@app.route('/trap/session-variables/')
def trap_session_variables():
    return render_template(
        'traps/parameters.html',
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
            year_mod = year
        else:
            year_mod = year % 10000
            if year_mod < 1:
                year_mod = 1
        cal_list = [cal.monthdatescalendar(year_mod, i + 1) for i in xrange(12)]
    except Exception, e:
        logConsole(e)
        abort(500)
    else:
        return render_template(
            'traps/calendar.html',
            year=year,
            calendar=cal_list
        )
    abort(501)


# @todo: implement this
@app.route('/trap/errors/')
def trap_errors():
    return render_template(
        'traps/errors.html',
        title=get_sentences(1, False)[0],
        content=get_sentences(random.randint(1, 5)),
        config=config
    )


# @todo: implement this
@app.route('/trap/deadends/')
def trap_deadends():
    return render_template(
        'traps/deadends.html',
        title=get_sentences(1, False)[0],
        content=get_sentences(random.randint(1, 5)),
        config=config
    )


# @todo: implement this
@app.route('/trap/comet/')
def trap_comet():
    return render_template(
        'traps/comet.html',
        title=get_sentences(1, False)[0],
        content=get_sentences(random.randint(1, 5)),
        config=config
    )


# @todo: implement this
@app.route('/trap/depth/')
def trap_depth():
    return render_template(
        'traps/depth.html',
        title=get_sentences(1, False)[0],
        content=get_sentences(random.randint(1, 5)),
        config=config
    )


@app.route('/success/', defaults={"challenge": None})
@app.route('/success/<string:challenge>')
def success(challenge):
    if not challenge:
        abort(500)
    else:
        return render_template(
            'success.html',
            title="Challenge "
                  + challenge
                  + " complete!",
            challenge=challenge
        )


@app.route('/fail/', defaults={"challenge": None})
@app.route('/fail/<string:challenge>')
def fail(challenge):
    if not challenge:
        abort(500)
    else:
        return render_template('fail.html', title="Challenge " + challenge + " failed!", challenge=challenge)


def url_for_other_page(page_number):
    """url_for helper function for pagination"""
    args = request.view_args.copy()
    args['page_number'] = page_number
    return url_for(request.endpoint, **args)


app.jinja_env.globals['url_for_other_page'] = url_for_other_page


@app.after_request
def per_request_callbacks(response):
    if not re.match(r'/admin(.*)', request.path, re.M | re.I):

        for func in getattr(g, 'call_after_request', ()):
            response = func(response)

        lr = LoggingRequest(
            datetime.today(),
            request.method,
            request.path,
            request.args.lists(),
            request.form.lists(),
            None if request.routing_exception is None
            else str(request.routing_exception),
            request.environ['HTTP_USER_AGENT']
        )

        str_to_log = lr.__dict__
        log_file.debug(str_to_log)

    return response


if __name__ == '__main__':
    init_db()
    app.run()
