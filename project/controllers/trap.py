from calendar import Calendar
from datetime import date
from os import abort
import random

from flask import render_template, request, session, flash, redirect, url_for, make_response
from flask.ext.wtf import Form
from loremipsum import get_sentences
from wtforms import TextField, validators

from project import app, config
from project.tools.logger import logConsole


__author__ = 'gableroux'


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


@app.route('/trap/errors/')
def trap_errors():
    return render_template(
        'traps/errors.html',
        title=get_sentences(1, False)[0],
        content=get_sentences(random.randint(1, 5)),
        config=config
    )


@app.route('/trap/deadends/')
def trap_deadends():
    return render_template(
        'traps/deadends.html',
        title=get_sentences(1, False)[0],
        content=get_sentences(random.randint(1, 5)),
        config=config
    )


@app.route('/trap/comet/')
def trap_comet():
    return render_template(
        'traps/comet.html',
        title=get_sentences(1, False)[0],
        content=get_sentences(random.randint(1, 5)),
        config=config
    )


@app.route('/trap/depth/')
def trap_depth():
    return render_template(
        'traps/depth.html',
        title=get_sentences(1, False)[0],
        content=get_sentences(random.randint(1, 5)),
        config=config
    )


@app.route('/trap/single_form', methods=['GET', 'POST'])
def trap_single_form():
    form = CreateForm(request.form)
    if request.method == 'POST' and form.validate():
        from project.models.Printer import Printer

        printer = Printer()
        printer.show_string(form.text.data)
        return render_template('printer/index.html')
    return render_template('printer/print.html', form=form)


class CreateForm(Form):
    text = TextField(u'Text:', [validators.Length(min=1, max=20)])