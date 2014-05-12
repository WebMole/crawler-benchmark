# -*- coding: utf-8 -*-
from project.configuration import Configuration
#from project.controllers.database import init_db

__version__ = '0.1'
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
import jinja2

app = Flask('project')
app.config['SECRET_KEY'] = 'a44eabc44ce37a66ad1871522f592a7e'
app.debug = True
toolbar = DebugToolbarExtension(app)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE='./db/main.db',
    DEBUG=True,
    SECRET_KEY='ls20f48g578hbmflgdi3',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
config = Configuration

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(Configuration.template_folder_path),
])
app.jinja_loader = my_loader

# Here because the "app" must exists first
from project.controllers.database import init_db

init_db()
#app.run()

from project.controllers import *
