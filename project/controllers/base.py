# -*- coding: utf-8 -*-
from os import abort

from flask import render_template

from project import app, config


@app.route('/')
def index():
    return render_template('index.html', modes=config.modes, title='Page selection')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('layout/404.html', title=e), 404


@app.route('/success/', defaults={"challenge": None})
@app.route('/success/<string:challenge>')
def success(challenge):
    if not challenge:
        abort(500)
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
        abort(500)
    else:
        return render_template('layout/fail.html', title="Challenge " + challenge + " failed!", challenge=challenge)
