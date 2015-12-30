#!/usr/bin/env python
# encoding: utf-8
import os.path
from flask import render_template, url_for
from app import app
from app.forms import *
from app.TextAnalyze import TextAnalyze
from jinja2 import Markup
  

@app.route('/')
@app.route('/index', methods=('GET', 'POST'))
def index():
#		return 'Hello, Flask!'
  form = WordFileForm()
  if form.validate_on_submit():
    filename = secure_filename(form.filename.data.filename)
#    tokens = nltk.word_tokenize(form.filename.data.read().decode('utf-8'))
#    wnl = nltk.WordNetLemmatizer()
#    fdist = FreqDist(wnl.lemmatize(wnl.lemmatize(word.lower()), 'v') for word in tokens if word.isalpha())
#    return render_template('words.html', article_title=filename, fdist = fdist)
    ta = TextAnalyze()
    content=form.filename.data.read().decode('ISO-8859-1')
    return render_template('words.html', article_title = filename, text=Markup('<p>'+content.replace('\r\n', r'</p><p>')[0:-3]), fdist=ta.getdict(content))
  return render_template('index.html', form = form)


@app.route('/article')
def article():
  req = urllib.request.urlopen('http://fanyi.youdao.com/openapi.do?keyfrom=myklory&key=1519925193&type=data&doctype=json&version=1.1&q=good')
  content = req.read().decode('utf-8') 
  c = MongoClient(host='localhost', port=27017)
  db = c.dict
  content = json.loads(content)
  content.pop('translation')
  content.pop('web')
  content.pop('query')
  content.pop('errorCode')
  content['word'] = 'good'
    
  db.basic.insert(content)
  return render_template('article.html', content=content)

@app.route('/words')
def words():
  filepath = os.path.abspath(os.path.dirname(__file__)) + url_for('static', filename='tmp/0100011.txt')
  with open(filepath, 'r') as f:
    content = f.read()
  tokens = nltk.word_tokenize(content)
  fdist = FreqDist(word.lower() for word in tokens if word.isalpha())
  print(type(fdist))
  return render_template('words.html', article_title='Animal Farm', wordscount=len(tokens), fdist=fdist)

from werkzeug import secure_filename
@app.route('/upload/', methods=('GET', 'POST'))
def upload():
  form = WordFileForm()
  if form.validate_on_submit():
    filename = secure_filename(form.filename.data.filename)
    tokens = nltk.word_tokenize(form.filename.data.read().decode('utf-8'))
    fdist = FreqDist(word.lower() for word in tokens if word.isalpha())
    return render_template('words.html', article_title=filename, fdist = fdist)
  else:
    return render_template('indtx.html')
  print(form.filename.data)
  return render_template('words.html', article_title=filename)

