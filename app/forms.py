#!/usr/bin/env python
# encoding: utf-8


from wtforms import FileField, StringField, PasswordField
from flask_wtf import Form

class UserForm(Form):
  username = StringField('User Name')
  password = PasswordField('Password')
  repeatpassword = PasswordField('Repeat Password')

class WordFileForm(Form):
  filename = FileField('Upload your file')
