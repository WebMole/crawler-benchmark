# -*- coding: utf-8 -*-
from wtforms import StringField, validators

from flask_wtf import Form, RecaptchaField


class recaptcha_form(Form):
    # text = StringField(u'Text:', [validators.Length(min=1, max=20)])
    recaptcha = RecaptchaField()