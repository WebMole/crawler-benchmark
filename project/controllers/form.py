# -*- coding: utf-8 -*-
from wtforms import validators

from flask_wtf import Form, RecaptchaField, StringField, PasswordField, BooleanField


class RecaptchaForm(Form):
    recaptcha = RecaptchaField()


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])
