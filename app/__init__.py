#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, url_for
from flask.ext.pymongo import PyMongo
from flask.ext.login import LoginManager
app = Flask(__name__)
app.config.from_object('config')

dictdb = PyMongo(app, config_prefix='DICT')
authdb = PyMongo(app, config_prefix='AUTH')

login_manager = LoginManager()
login_manager.init_app(app)
from app import views

login_manager.login_view = "signin"
