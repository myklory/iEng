#!/usr/bin/env python
# encoding: utf-8

import nltk
from nltk import FreqDist
import urllib
import sys
import json
from pymongo import MongoClient
from time import clock
from app import dictdb
class TextAnalyze():

  def getremotedict(self, word):
    try:
      req = urllib.request.urlopen('http://fanyi.youdao.com/openapi.do?keyfrom=myklory&key=1519925193&type=data&doctype=json&version=1.1&q=' + word)
      content = req.read().decode('utf-8') 
      content = json.loads(content)
      if content['errorCode'] != 0 or 'basic' not in content:
        return None
      #c = MongoClient(host='localhost', port=27017)
      #db = c.dict
      if 'translation' in content:
        content.pop('translation')
      if 'web' in content:
        content.pop('web')
      if 'query' in content:
        content.pop('query')
      if 'errorCode' in content:
        content.pop('errorCode')
      content['word'] = word
      #db.basic.insert(content)
      dictdb.db.basic.insert(content)
      return content
    except:
      return None

  def getexp(self, word):
   # c = MongoClient(host='localhost', port=27017)
   # db = c.dict
   # exp = db.basic.find_one({'word':word})
    #print(word)
    exp = dictdb.db.basic.find_one({'word': word})
    if exp == None:
      exp = self.getremotedict(word)
    #print(word,exp)
    return exp

  def getdict(self, content):
    wnl = nltk.WordNetLemmatizer()
    begin = clock()
    print('begin')
    tokens = nltk.word_tokenize(content)
    wordlist = nltk.corpus.words.words()
    stopwords = nltk.corpus.stopwords.words('english')
    fdist = FreqDist(wnl.lemmatize(wnl.lemmatize(wnl.lemmatize(word.lower(),'a')), 'v') for word in tokens if word.isalpha() and word not in stopwords)
    print(clock() - begin)
    js = {'samples': fdist.B(), 'outcomes': fdist.N()}
    wdict = {}
    count = 1
    begin = clock()
    for w in fdist.most_common():
      d = {'index': count, 'word': w[0], 'count': w[1], 'freq': round(fdist.freq(w[0]), 4)}
      d['basic'] = self.getexp(w[0])
      wdict[w[0]] = d
      count = count + 1
    print(clock() - begin)
    wdict = sorted(wdict.items(),key=lambda t: t[1]['index'])
    js['words'] = wdict
    return js
