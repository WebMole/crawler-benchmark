# -*- coding: utf-8 -*-
from os import abort
from flask import session, flash, redirect, url_for, request, render_template
from loremipsum import get_sentences, get_paragraphs
from project import app, config, init_db
from project.controllers import GraphManager
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

    output = GraphManager.draw_custom_graph(user_agents=request.values.getlist('selUserAgent'))
    response = make_response(output.getvalue())
    response.mimetype = 'image/svg+xml'
    return response


@app.route('/admin/clear_log_user_agents', methods=['DELETE'])
def clear_log_user_agents():
    logger.clear_log(user_agents=request.values.getlist('selUserAgent'))
    return "OK"


@app.route('/admin/results')
def results():
    return render_template(
        "admin/results.html",
        user_agents=logger.get_log_user_agents(),
        in_admin=True
    )


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