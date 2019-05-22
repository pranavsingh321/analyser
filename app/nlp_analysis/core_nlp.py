from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import stanfordnlp as snlp
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flair.embeddings import WordEmbeddings, FlairEmbeddings
from flair.embeddings import  StackedEmbeddings, BertEmbeddings
from flair.embeddings import DocumentPoolEmbeddings
import polyglot
from polyglot.text import Text, Word
from polyglot.transliteration import Transliterator
from polyglot.downloader import downloader
from polyglot.detect import Detector
from langdetect import detect
import RAKE
from babel import Locale
from nltk.corpus import stopwords

from nltk import FreqDist
from nltk.corpus import brown
from app.constants import *


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)

def detect_language(sentence):
    detected_language = Detector(sentence)
    language_code = detected_language.language.code
    if not detect_language.reliable:
        # if not sure use langdetect
        language_code = detect(sentence)

    if language not in cs.LANGUAGES_LIST:
        language = SWEDISH
    return language_code 


def translate_language(source, destination, text):
    transliterator = Transliterator(source_lang="en", target_lang="ru")
    return transliterator.transliterate(text)


def freq_distribution(word):
    # Get the word's  expression in terms of frequency distribution
    fdist = FreqDist(brown.words())
    fdist['good']

def keywords_analysis(text_data, language):
    complete_language_name = Locale(language).english_name.lower()
    Rake = RAKE.Rake(stopwords.words(complete_language_name))
    return Rake.run(text_data)


class ContextualAnalysis:

    def __init__(self, text_data, language):
        self.processors = 'tokenize, mwt, lemma, pos, depparse'
        self.pipeline = snlp.Pipeline(lang=language, processors=self.processors)

    def context_based_tree(self, content):
        processed_doc = self.pipeline(content)
        for sentence in processed_doc.sentences:
           # TODO the relation between adjectives and noun/adverb
           pass


class SentimentAnalysis:

     def __init__(self, text, language):
         self.text_data = text
         self.language = language

     def get_consolidated_rating(self):
        # if self.language == ENGLISH:
        #     analyser = SentimentIntensityAnalyzer()
        #     return round(analyser.polarity_scores(complete_corpus)['compound'] * 10)
        # else:
        #swedish sentiment analysis
        overall_sentiment = 0
        text = Text(self.text_data)
        for sentence in text.sentences:
            overall_sentiment += sentence.polarity

        return int(overall_sentiment/len(text.sentences)) * 10


class EntitySentimentRecognition:

     def __init__(self, text_data, language):
         self.text_data = text_data
         self.entities_sentiment = {}
         self.language = language

     def normalize_sentiment_number(self, positive_sentiment, negative_sentiment):
         _positive = round(positive_sentiment * 10)
         _negative = round(negative_sentiment * 10)
         if _positive >= _negative:
             _result = 5 + _positive -_negative
         else:
             _result = 5 - (_negative - _positive)

     def extract_entities(self,):
         entities_data = []
         data = Text(self.text_data, hint_language_code=self.language)
         for entity in data.entities:
             str_entity = ' '.join(entity.copy())
             self.entities_sentiment[str_entity] = self.normalize_sentiment_number(entity.positive_sentiment,
                                                                                   entity.negative_sentiment)

         return self.entities_sentiment

         #https://www.depends-on-the-definition.com/named-entity-recognition-with-bert/
           # or user corenlp for ner
           # use spacy
           #https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
