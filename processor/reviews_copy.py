
from __future__ import division

import re

from six import string_types
import pandas as pd
import numpy as np
import seaborn as sns
import nltk
from nltk.corpus import StopWords

from nltk.tokenize import sent_tokenize
from nltk.corpus import wordnet as wn
from langdetect import detect

TITLE = re.compile(r'^\[t\](.*)$')  # [t] Title
FEATURES = re.compile(
    r'((?:(?:\w+\s)+)?\w+)\[((?:\+|\-)\d)\]'
)  # find 'feature' in feature[+3]
NOTES = re.compile(r'\[(?!t)(p|u|s|cc|cs)\]')  # find 'p' in camera[+2][p]
SENT = re.compile(r'##(.*)$')  # find tokenized sentence


bow_transformer = CountVectorizer(analyzer=text_process).fit(X)
len(bow_transformer.vocabulary_)
review_25 = X[24]
bow_25 = bow_transformer.transform([review_25])
print(bow_transformer.get_feature_names()[11443])
print(bow_transformer.get_feature_names()[22077])
X = bow_transformer.transform(X)

from sklearn.feature_extraction.text import CountVectorizer
corpus = [
    'This is the first document.',
    'This document is the second document.',
    'And this is the third one.',
    'Is this the first document?',
]
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)
print(vectorizer.get_feature_names())

from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()
nb.fit(X_train, y_train)
#@compat.python_2_unicode_compatible
class Review(object):
    """
    A Review is the main block of a ReviewsCorpusReader.
    """

    def __init__(self, title=None, review_lines=None):
        self.title = title
        if review_lines is None:
            self.review_lines = []
        else:
            self.review_lines = review_lines

    def add_line(self, review_line):
        assert isinstance(review_line, ReviewLine)
        self.review_lines.append(review_line)


    def features(self):
        features = []
        for review_line in self.review_lines:
            features.extend(review_line.features)
        return features


    def sents(self):
        return [review_line.sent for review_line in self.review_lines]


    def __repr__(self):
        return 'Review(title=\"{}\", review_lines={})'.format(
            self.title, self.review_lines
        )

    def words(self, fileids=None):
        return concat(
            [
                self.CorpusView(path, self._read_word_block, encoding=enc)
                for (path, enc, fileid) in self.abspaths(fileids, True, True)
            ]
        )


    def _read_features(self, stream):
        features = []
        for i in range(20):
            line = stream.readline()
            if not line:
                return features
            features.extend(re.findall(FEATURES, line))
        return features


#@compat.python_2_unicode_compatible
class ReviewLine(object):

    def __init__(self, sent, features=None, notes=None):
        self.sent = sent
        if features is None:
            self.features = []
        else:
            self.features = features

        if notes is None:
            self.notes = []
        else:
            self.notes = notes

    def __repr__(self):
        return 'ReviewLine(features={}, notes={}, sent={})'.format(
            self.features, self.notes, self.sent
        )

class Lookup():

    def __init__(self):
        self.antonyms = {}
        self.synonyms = {}

    def get_antonyms(self):
        kfjsdko
    def get_synonyms(self)
        jsdlkfjdsl


class ReviewsReader():


    def __init__(
        self, root, fileids, word_tokenizer=WordPunctTokenizer(), encoding='utf8'
    ):
        self.language = 'eng'

   def detect_language(text)
      self.language =  detect(text)
        .__init__(self, root, fileids, encoding)
        self._word_tokenizer = word_tokenizer
   def 
   wn.synsets(b'\xe7\x8a\xac'.decode('utf-8'), lang='jpn')
   print(sent_tokenize(mytext,"french"))
    def raw(self, fileids=None):
        if fileids is None:
            fileids = self._fileids
        elif isinstance(fileids, string_types):
            fileids = [fileids]
        return concat([self.open(f).read() for f in fileids])




    def _read_review_block(self, stream):
            review_line = ReviewLine(sent=sent, features=feats, notes=notes)
            review.add_line(review_line)

    def _read_sent_block(self, stream):
        sents = []
        for review in self._read_review_block(stream):
            sents.extend([sent for sent in review.sents()])
        return sents

    def _read_word_block(self, stream):
        words = []
        for i in range(20):  # Read 20 lines at a time.
            line = stream.readline()
            sent = re.findall(SENT, line)
            if sent:
                words.extend(self._word_tokenizer.tokenize(sent[0]))
        return words


