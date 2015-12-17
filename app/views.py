#!/usr/bin/env python
# encoding: utf-8
from flask import render_template
from app import app
@app.route('/')
@app.route('/index')
def index():
#		return 'Hello, Flask!'
    return render_template('base.html')
