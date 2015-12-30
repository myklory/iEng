#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask.ext.pymongo import PyMongo
app = Flask(__name__)
app.config.from_object('config')

dictdb = PyMongo(app, config_prefix='DICT')
from app import views
