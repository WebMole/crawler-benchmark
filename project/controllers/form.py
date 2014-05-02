# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, validators


class CreateForm(Form):
    text = TextField(u'Text:', [validators.Length(min=1, max=20)])