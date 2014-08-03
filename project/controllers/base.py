# -*- coding: utf-8 -*-

from flask import render_template, url_for, request, make_response

from project import app, config
from project.controllers.form import RecaptchaForm


@app.route('/')
def index():
    return render_template('index.html', modes=config.modes, title='Home')


@app.route('/print', methods=['GET', 'POST'])
def printer():
    form = RecaptchaForm(request.form)
    if request.method == 'POST' and form.validate():
        from project.models.Printer import Printer

        printer = Printer()
        printer.show_string(form.text.data)
        return render_template('printer/index.html')
    return render_template('printer/print.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('layout/404.html', title=e), 404


@app.route('/success/', defaults={"challenge": None})
@app.route('/success/<string:challenge>')
def success(challenge):
    if not challenge:
        return make_response(render_template("layout/500.html", message="Challenge must be set"), 500)
    else:
        return render_template(
            'layout/success.html',
            title="Challenge "
                  + challenge
                  + " complete!",
            challenge=challenge
        )


@app.route('/fail/', defaults={"challenge": None})
@app.route('/fail/<string:challenge>')
def fail(challenge):
    if not challenge:
        return make_response(render_template("layout/500.html", message="Challenge must be set"))
    else:
        try:
            message = request.args['message']
        except KeyError:
            message = None

    return render_template(
        'layout/fail.html',
        title="Challenge " + challenge + " failed!",
        challenge=challenge,
        message=message
    )


def url_for_other_page(page_number):
    """url_for helper function for pagination"""
    args = request.view_args.copy()
    args['page_number'] = page_number
    return url_for(request.endpoint, **args)


app.jinja_env.globals['url_for_other_page'] = url_for_other_page

