#!/usr/bin/env python
# encoding: utf-8

import hashlib
from flask import render_template, url_for, request
from app import app, authdb
from app.forms import *
from flask.ext.login import login_required

  
'''
@app.route('/')
@app.route('/index', methods=('GET', 'POST'))
def index():
		return 'Hello, Flask!'
  form = WordFileForm()
  if form.validate_on_submit():
    filename = secure_filename(form.filename.data.filename)
    tokens = nltk.word_tokenize(form.filename.data.read().decode('utf-8'))
    wnl = nltk.WordNetLemmatizer()
    fdist = FreqDist(wnl.lemmatize(wnl.lemmatize(word.lower()), 'v') for word in tokens if word.isalpha())
    return render_template('words.html', article_title=filename, fdist = fdist)
    ta = TextAnalyze()
    content=form.filename.data.read().decode('ISO-8859-1')
    return render_template('words.html', article_title = filename, text=Markup('<p>'+content.replace('\r\n', r'</p><p>')[0:-3]), fdist=ta.getdict(content))
  return render_template('index.html', form = form)
'''


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signup', methods=('POST','GET'))
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        pwdmd5 = hashlib.md5()
        pwdmd5.update((form.password.data + form.email.data).encode('utf-8'))
        new = {'nickname' : form.nickname.data, 'email' : form.email.data, 'password' : pwdmd5.hexdigest()}
        #authdb.db.users.insert(new)
        user = User()
        user.nickname = form.nickname.data
        user.email = form.email.data
    return render_template('signup.html', form=form)

@app.route('/validateemail', methods=('POST', 'GET'))
def validateemail():
    email = request.form['email']
    ret = authdb.db.users.find_one({'email':email})
    if ret is not None:
        return 'false'
    else:
        return 'true'

@app.route('/validatenickname', methods=('POST', 'GET'))
def validatenickname():
    nickname = request.form['nickname']
    ret = authdb.db.users.find_one({'nickname':nickname})
    print(ret)
    if ret is not None:
        return 'false'
    else:
        return 'true'