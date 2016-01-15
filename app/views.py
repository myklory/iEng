#!/usr/bin/env python
# encoding: utf-8

import hashlib
import nltk
from flask import flash
from flask import redirect
from flask import render_template, url_for, request
from app import app, authdb, login_manager
from app.forms import *
from flask.ext.login import login_required, login_user, logout_user, current_user
from app.models import User
from markupsafe import Markup
from werkzeug.utils import secure_filename
from nltk import FreqDist
from app.TextAnalyze import TextAnalyze

@app.route('/')
@app.route('/index', methods=('GET', 'POST'))
@login_required
def words():
  form = WordFileForm()
  if form.validate_on_submit():
    filename = secure_filename(form.filename.data.filename)
    #tokens = nltk.word_tokenize(form.filename.data.read().decode('utf-8'))
    #wnl = nltk.WordNetLemmatizer()
    #fdist = FreqDist(wnl.lemmatize(wnl.lemmatize(word.lower()), 'v') for word in tokens if word.isalpha())
    ta = TextAnalyze()
    content=form.filename.data.read().decode('ISO-8859-1')
    return render_template('index.html',
                           form = form,
                           isAnalyze=True,
                           article_title = filename,
                           text=Markup('<p>'+content.replace('\r\n', r'</p><p>')[0:-3]),
                           fdist=ta.getdict(content))
  return render_template('index.html', form = form, isAnalyze=False)


'''
@app.route('/')
@app.route('/index')
@login_required
def index():
    form = WordFileForm()
    return render_template('index.html', form = form)
'''

@app.route('/signin', methods=['POST', 'GET'])
def signin():
    form = SigninForm()

    if form.validate_on_submit():
        pwdmd5 = hashlib.md5()
        pwdmd5.update((form.password.data + form.email.data).encode('utf-8'))
        u = authdb.db.users.find_one({'email':form.email.data})
        if u is not None and u['password'] == pwdmd5.hexdigest():
            user = User(u['nickname'])
            login_user(user)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid email or password, please try again.')
    return render_template('signin.html', form = form)


@app.route('/signup', methods=('POST','GET'))
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        pwdmd5 = hashlib.md5()
        pwdmd5.update((form.password.data + form.email.data).encode('utf-8'))
        new = {'nickname' : form.nickname.data, 'email' : form.email.data, 'password' : pwdmd5.hexdigest()}
        authdb.db.users.insert(new)
        user = User(form.nickname.data)
        login_user(user)
        redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(nickname):
    return User(nickname)

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