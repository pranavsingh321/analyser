import stanfordnlp as snlp
# from app.models import CampaignAnalysis
from gensim.utils import simple_preprocess

import app.constants as cs
import core_nlp as cn
from core_nlp import SentimentAnalysis, FeatureExtract, ContextualAnalysis
from core_nlp import detect_language
import nlp_analysis.filters as fl


"""
Read the reviw
 Get the emoji review sentiment
 Clean up the data, emoji, unwanted chars, stopwords(detect language)
 detegct language using polyglot detect and if fails use langdetect fallback swedish
 Chaneg the review int lines
 Create the lemma
 Check the entities using polygot
1)Find the topics in the review text and corresponding(LDA)
2) Use Stanford NLP for the sentence split and use dependency parser for the adjectives using regex
2) Use the  Flair with embedding for topic r
{
  'event_id': 'hash',
  'event_rating': int,
  'event_sentiment_summary' : {},
  'event_entities': ['', ''],
  'event_topics': ['', ''],
  'reviews': [
      {
       'review_id': 'hash',
       'review_rating': int,
       'review_raw_sentiment' : {},
       'review_sentiment_summary' : {},
       'review_entities': ['', ''],
       'review_topics': ['', ''],
       'review_language': 'en',
       'lines': [
          {
            'line_index':int,
            'line_raw_sentiment':{},
            'line_entities_sentiment': [{}, {}, {}],
            'line_topics': []
          }
         ]
       },
       {
        #Another review
       }
    ]

}
"""


class ReviewLine:
    """
    A ReviewLine represents a sentence of the review, together with
    annotations of its features.
    """

    def __init__(self, sentence, topics, language):
        self.sentence = sentence
        self.language = language
        self.context_analysis = ContextualAnalysis(sent, language)
        self.line_entities_sentiment = {}
        self.line_topics = topics

    def get_entities_sentiment(self,):
        # Get the entities and their correspoding sentiment
        return EntitySentimentRecognition(self.sentence, self.language).extract_entities()

    def get_topics_sentiment(self,):
        # Get the entities and their correspoding sentiment
        topics_sentiment = {}
        for topic in self.line_topics:
            if topic in self.sentence:
                 sentiment_analyser = SentimentAnalysis(self.review_text, self.language)
                 topics_sentiment[topic] = sentiment_analyser.get_consolidated_rating()

        return topics_sentiment


class Review:
    """
    A Review is the main block of a ReviewsReader.
    """

    def __init__(self, review, topics, rating=None, language=None):
        self.review_language = language if language else detect_language(review)
        self.review_text = fl.filter_contents(review, filters_pipeline='lemma',
                                              lang=self.review_language)
        self.review_id = uuid.UUID()
        self.review_rating = rating
        self.review_sentiment_summary = None
        self.review_entities = None
        self.review_topics = topics
        self.sentences = None

    def get_lines_in_review(self,):
        # Use stanfordnlp to get the lines in review
        self.sentences = snlp.sel
        return []

    def get_sentiment_rating(self,):
        sentiment_analyser = SentimentAnalysis(self.review_text, self.language)
        return sentiment_analyser.get_consolidated_rating()

    def generate_object(self,):
        for line in self.get_lines_in_review():
            rl = ReviewLine(line, self.topics, self.review_language)
            self.review_entities = rl.get_entities_sentiment()
            self.review_topics = rl.get_topics_sentiment()

        return {
                'review_id': self.review_id,
                # 'review_rating': int, TODO
                'review_sentiment' : self.get_sentiment_rating(),
                'review_entities': self.review_entities,
                'review_topics': self.review_topics,
                'review_language': self.review_language,
               }


class EventReviews:
    """
    Main reviews reader, starting point of processing
    """


    def __init__(self, reviews_list, language=None):
        """
        :param root: The root directory for the corpus.
        """
        self.language = language
        # TODO Do the emoji cleanup and lemmatize
        self.reviews_list = reviews_list
        self.processors = 'tokenize, mwt, lemma , pos, depparse'
        self.sentiment_analyser = SentimentAnalysis()
        self.complete_corpus = ''.join(self.reviews_list).lower()
        self.complete_corpus = fl.filter_contents(content=self.complete_corpus, filters_pipeline='emoji')
        self.keywords = self.get_keywords()

    def get_dependency(self,):
        # TODO remove this fucntion
        snlp = stanfordnlp.Pipeline(self.language, processors=self.processors)
        analysed_data = snlp(self.complete_corpus)

    def get_sentiment_rating(self):
        sentiment_analyser = SentimentAnalysis(self.complete_corpus, self.language)
        return sentiment_analyser.get_consolidated_rating()

    def get_keywords(self):
        return cn.keyword_analysis(self.complete_corpus)

    def get_average(self, list_data):
        _keys_count, _keys_avg = {}, {}
        for data in list_data:
            for key, value in data.items():
                if key in _keys:
                    _keys_count[key] += 1
                    _keys_avg[key] += value
                else:
                     _keys_count[key] = 1
                     _keys_avg[key] = value
        return {key: (value/_keys_count[key]) for key, value in _keys_avg}


    def generate_object(self,):
        _reviews, _keywords, _entities = [], [], []

        for review in self.clean_reviews_list:
             review_data = Review(self.language, self.get_keywords).generate_object()
             #TODO get the named entities
             _entities.append(review['review_entities'])
             _keywords.append(review['review_topics'])
             _reviews.append(review_data)

        keywords_avg = get_average(_keywords)
        entities_avg = get_average(_entities)

        return {
                'event_id': 'hash',
                'event_rating': self.get_sentiment_rating(),
                'event_summary' : {}, #TODO the textrank
                'event_entities': entities_avg,
                'event_topics': keywords_avg,
                'reviews': _reviews
               }
