#!/usr/bin/env python
# encoding: utf-8
from app import app
if __name__ == "__main__":
    app.run(debug = True)
else:
    import nltk
    nltk.data.path.append('/home/namine/nltk_data')
