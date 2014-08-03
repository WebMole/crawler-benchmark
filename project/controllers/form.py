# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, validators


class CreateForm(Form):
    text = StringField(u'Text:', [validators.Length(min=1, max=20)])