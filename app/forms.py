#!/usr/bin/env python
# encoding: utf-8


from wtforms import FileField, StringField, PasswordField, validators
from wtforms.validators import Email
from flask_wtf import Form

class SignupForm(Form):
  username = StringField('User Name', validators=[Email(message='That is not a valid email address.')])
  nickname = StringField('Nick Name', validators=[validators.DataRequired(), validators.Length(min=4)])
  password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=6)])
  repeatpassword = PasswordField('Repeat Password', validators=[validators.InputRequired(), validators.EqualTo('password', message='Passwords must match')])

class WordFileForm(Form):
  filename = FileField('Upload your file')
