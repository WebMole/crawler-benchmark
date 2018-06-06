# -*- coding: utf-8 -*-
from os import abort
import json

from flask import session, flash, redirect, url_for, request, render_template, Response
from loremipsum import get_sentences, get_paragraphs

from project import app, config, init_db
from project.controllers import graph
from project.controllers.database import get_db
from project.tools import logger
from project.tools.tools import get_specific_item


@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/admin/plot.svg')
def plot():
    from flask import make_response

    output = graph.draw_custom_graph(user_agents=request.values.getlist('selUserAgent'))
    response = make_response(output.getvalue())
    response.mimetype = 'image/svg+xml'
    return response


@app.route('/admin/clear_log_user_agents', methods=['DELETE'])
def clear_log_user_agents():
    logger.clear_log(user_agents=request.values.getlist('selUserAgent'))
    return "OK"


@app.route('/admin/user_agents', methods=['GET'])
def get_user_agents():
    return Response(json.dumps(logger.get_log_user_agents()), mimetype='application/json')


@app.route('/admin/results')
def results():
    return render_template(
        "admin/results.html",
        user_agents=logger.get_log_user_agents(),
        successes=logger.get_log_dicts_success(),
        failures=logger.get_log_dicts_failure(),
        in_admin=True
    )


@app.route('/admin/logs')
@app.route('/admin/logs/<int:limit>')
def logs(limit=None):
    if (limit is None):
        last_n_lines_to_pass = config.log_view_n_lines
    else:
        last_n_lines_to_pass = limit
    return render_template(
        "admin/logs.html",
        logs=logger.get_log_dicts(last_n_lines=last_n_lines_to_pass),
        log_view_n_lines=last_n_lines_to_pass,
        in_admin=True
    )


@app.route('/admin/logs/full')
def logs_full():
    return render_template(
        "admin/logs.html",
        logs=logger.get_log_dicts(),
        log_view_n_lines="all",
        in_admin=True
    )


@app.route("/admin/clear/<string:mode>", methods=['DELETE'])
def clear_entries(mode):
    """Creates the database tables."""
    with app.app_context():
        db = get_db()

        database_request = "drop table if exists " + mode + ";"
        db.cursor().executescript(database_request)
        db.commit()
        init_db()

        flash('All ' + mode + ' entries were successfully cleared')
        return "OK"


@app.route("/admin/add/<string:mode>/<int:num>", methods=['POST'])
def entries_add_auto(mode, num):
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    for i in range(0, num):
        db.execute(
            'insert into ' + mode +
            ' (title, text) values (?, ?)',
            [get_sentences(1, False)[0].replace(".", ""), get_paragraphs(1, False)[0]]
        )
    db.commit()
    flash('New ' + mode + ' automatic %d %s entrie%s successfully posted' %
          (num, mode, 's were' if (num > 1) else ' was'))
    return "OK"


@app.route("/admin/add/<string:mode>", methods=['POST'])
def entries_add(mode):
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    db.execute('insert into ' + mode + ' (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New ' + mode + ' entry was successfully posted')
    return "OK"


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
    return render_template('layout/login.html', error=error)


@app.route("/admin/mode/<string:mode>", methods=['GET'])
def get_mode(mode):
    db = get_db()
    for tmp_mode in config.modes:
        cur = db.execute('select count(id) from ' + tmp_mode.get("route"))
        count = cur.fetchone()
        tmp_mode.__setitem__('count', count[0])

    mode = get_specific_item(config.modes, "route", mode)

    return render_template(
        "admin/modes.html",
        mode=mode,
        in_admin=True
    )


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
