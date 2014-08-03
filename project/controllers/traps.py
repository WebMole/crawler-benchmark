from calendar import Calendar
from datetime import date
import random

from flask import render_template, request, session, flash, redirect, url_for, make_response
from loremipsum import get_sentences

from project import app, config
from project.tools.logger import logConsole
from form import recaptcha_form


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
        title="Login Trap",
        error=error,
        config=config
    )


@app.route('/trap/outgoing/')
def trap_outgoing():
    return render_template(
        'traps/outgoing.html',
        title="Outgoing links Trap",
        config=config,
        links=config.links["external"],
        next=url_for("success", challenge="outgoing")
    )


@app.route('/trap/parameters/')
def trap_parameters():
    return render_template(
        'traps/parameters.html',
        title="@todo: Parameters, ask to manually insert a parameter?",
        config=config
    )


@app.route('/trap/cookies/')
def trap_cookies():
    resp = make_response(
        render_template(
            'traps/cookies.html',
            title="We just stored a cookie value for 'crawler_stores_cookies'",
            config=config
        )
    )
    resp.set_cookie('crawler_stores_cookies', 'yes')
    # @todo: Check later if 'crawler_stores_cookies' is set
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
        title="@todo: Session variables, we will set some session variable and check later if it is set",
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
            year_mod = year % 9999
            if year_mod < 1:
                year_mod = 1
        cal_list = [cal.monthdatescalendar(year_mod, i + 1) for i in xrange(12)]
    except Exception, e:
        logConsole(e)
    else:
        return render_template(
            'traps/calendar.html',
            year=year,
            calendar=cal_list
        )
    return make_response(render_template("layout/500.html"), 500)


@app.route('/trap/errors/')
def trap_errors():
    return render_template(
        'traps/errors.html',
        title="Do you support errors?",
        config=config
    )


@app.route('/trap/errors/<int:error_code>/')
def trap_error(error_code):
    # default error name, will be updated if exists in config error codes
    error_name = "Error code not defined"

    for error in config.error_codes:
        for code, name in config.error_codes[error]:
            if code == error_code:
                error_name = name

    return make_response(
        render_template("traps/error.html", error_code=error_code, error_name=error_name),
        error_code
    )


@app.route('/trap/deadends/')
def trap_deadends():
    return render_template(
        'traps/deadends.html',
        title="@todo: Deadends",
        config=config
    )


@app.route('/trap/comet/')
def trap_comet():
    return render_template(
        'traps/comet.html',
        title="@todo: comet",
        config=config
    )


@app.route('/trap/depth/')
@app.route('/trap/depth/<path:current_path>')
def trap_depth(current_path=""):
    # Starts at 2 because of initial deth: trap/depth/
    if current_path == "":
        next_path = "3/"
        current_depth = 2
        next_depth = str(current_depth + 1)
    else:
        current_depth = len(current_path.split("/")) + 1
        next_depth = str(current_depth + 1)
        next_path = current_path + next_depth + "/"

    if config.trap_deth_max_depth == -1 or current_depth <= config.trap_deth_max_depth:
        title = "current depth: " + str(current_depth)

        if config.trap_deth_max_depth != -1:
            title += ", max_depth: " + str(config.trap_deth_max_depth)

        return render_template(
            'traps/depth.html',
            title=title,
            content=get_sentences(random.randint(1, 5)),
            config=config,
            current_path=current_path,
            next_path=next_path,
            next_depth=next_depth
        )

    else:
        message = "You have reached max depth (config.trap_deth_max_depth): " + str(config.trap_deth_max_depth)
        return redirect(url_for('fail', challenge="depth", message=message))


@app.route('/trap/recaptcha', methods=['GET', 'POST'])
def trap_recaptcha():
    if app.config['RECAPTCHA_PUBLIC_KEY'] == "" or app.config['RECAPTCHA_PRIVATE_KEY'] == "":
        return make_response(
            render_template(
                'layout/500.html',
                message="You must set RECAPTCHA_PUBLIC_KEY and RECAPTCHA_PRIVATE_KEY in project's __init__.py first"
            ), 500
        )
    else:
        form = recaptcha_form(request.form, csrf_enabled=False)

        if request.method != 'POST':
            return render_template('traps/recaptcha.html', form=form)
        elif form.validate():
            return redirect(url_for('success', challenge="recaptcha"))
        else:
            return redirect(url_for('fail', challenge="recaptcha", message='recaptcha did not validate'))


@app.route('/trap/recaptcha', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data, form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)