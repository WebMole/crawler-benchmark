# -*- coding: utf-8 -*-
from project.configuration import Configuration
from project.configuration.utils import env_var
from project.models import db

__version__ = '0.1'
from flask import Flask
import jinja2

app = Flask('project')

# You can play with the settings below

app.debug = env_var('DEBUG', True)
app.debug_toolbar = env_var('DEBUG_TOOLBAR', False)
app.testing = env_var('TESTING', False)  # set to true so recaptcha always validate

app.config.update(dict(
    DATABASE='./db/main.db',
    DEBUG=app.debug,
    TESTING=app.testing,
    SECRET_KEY=env_var('SECRET_KEY'),
    USERNAME=env_var('BENCHMARK_USERNAME', 'admin'),
    PASSWORD=env_var('BENCHMARK_PASSWORD', 'default'),
    # To get your keys: https://www.google.com/recaptcha/admin#whyrecaptcha
    RECAPTCHA_USE_SSL=env_var('RECAPTCHA_USE_SSL', False),
    RECAPTCHA_PUBLIC_KEY=env_var('RECAPTCHA_PUBLIC_KEY', ''),
    RECAPTCHA_PRIVATE_KEY=env_var('RECAPTCHA_PRIVATE_KEY', ''),
    RECAPTCHA_OPTIONS=env_var('RECAPTCHA_OPTIONS', ''),
    SQLALCHEMY_TRACK_MODIFICATIONS=env_var('SQLALCHEMY_TRACK_MODIFICATIONS', False)

))

POSTGRES = {
    'user': env_var('DATABASE_USER'),
    'pw': env_var('DATABASE_PASSWORD'),
    'db': env_var('DATABASE_NAME'),
    'host': env_var('DATABASE_HOST'),
    'port': env_var('DATABASE_PORT', '5432'),
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

# Application goodies bellow, should not be edited
# Load default config and override config from an environment variable
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

if app.debug and app.debug_toolbar:
    from flask_debugtoolbar import DebugToolbarExtension

    toolbar = DebugToolbarExtension(app)

config = Configuration

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(Configuration.template_folder_path),
])
app.jinja_loader = my_loader

from project.controllers import *