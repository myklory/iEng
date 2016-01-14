#!/usr/bin/env python
# encoding: utf-8
from app import authdb
from wtforms import FileField, StringField, PasswordField, validators, ValidationError
from wtforms.validators import Email
from flask_wtf import Form

class SignupForm(Form):
  email = StringField('Email Address', validators=[Email(message='That is not a valid email address.')])
  nickname = StringField('Nick Name', validators=[validators.DataRequired(), validators.Length(min=2)])
  password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=6)])
  repeatpassword = PasswordField('Repeat Password', validators=[validators.InputRequired(), validators.EqualTo('password', message='Passwords must match')])

  def validate_email(form, field):
    ret = authdb.db.users.find_one({'email':field.data})
    if ret is not None:
      raise ValidationError("The Email is already registered!")

  def validate_nickname(form, field):
    ret = authdb.db.users.find_one({'nickname':field.data})
    if ret is not None:
      raise ValidationError("The nickname is already used!")

class SigninForm(Form):
  email = StringField('Email Address', validators=[validators.DataRequired(), Email(message='The Email Address is invalid.')])
  password = PasswordField('Password', validators=[validators.DataRequired()])
'''
  def validate_email(form, field):
    ret = authdb.db.users.find_one({'email':field.data})
    if ret is None:
      raise ValidationError("The Email is not registered!")
'''
class WordFileForm(Form):
  filename = FileField('Upload your file')
