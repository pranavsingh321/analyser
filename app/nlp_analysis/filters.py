import re
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from emoji import UNICODE_EMOJI
import stanfordnlp as snlp
from fuzzywuzzy import fuzz


SENTIMENT_CLASSES = ('bad', 'ok', 'good')
SWEDISH_ENGLISH_TRANSLATE = {SENTIMENT_CLASSES[0]:'dålig', SENTIMENT_CLASSES[1]:'ok', SENTIMENT_CLASSES[2]:'Bra'}


class StopWordsRemover():

    def __init__(self, language):
        self.stopwords_set = set(stopwords.words(language))

    def cleanup(self, content):
        return " ".join(word for word in content.split()
                        if word not in self.stopwords_set)


class LemmaFormatter:

    def __init__(self, language):
        self.language = language
        self.pipeline = snlp.Pipeline(processors='lemma', lang=self.language)

    def cleanup(self, content):
        return self.pipeline(content)


class UnwantedCharsRemover():

    def __init__(self):
        self.unwanted_chars = '?.,!:;"$%^&*()#@+/<>=\\[]_~{}|`'

    def cleanup(self, content):
        return content.translate({ord(c): None for c in self.unwanted_chars})


class StringSimilarity:

    def __init__(self, words_list):
        self.list_words = words_list

    def find_closest_word(self, match_word):
        """
        Find the closest word matching to the specific word
        """
        max_ratio, index = -1, None
        for word in self.list_words:
            ratio = fuzz.token_set_ratio(match_word, word)
            if ratio > max_ratio:
                max_ratio = ratio

        if int(max_ratio) > 80:
            return  self.list_words[index]

        return match_word

class RepeatCharsRemover():

    def __init__(self, text, language):
        self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'
        self.text  = text
        self.language = language

    def cleanup(self):
        return " ".join(self.replace_remover(word)
                        for word in self.text.split())

    def replace_remover(self, word):
        if wordnet.synsets(word, lang=self.language):
            return word
        repl_word = self.repeat_regexp.sub(self.repl, word)
        if repl_word != word:
            return self.replace_remover(repl_word)
        else:
            return repl_word


class EmojiRemover():
    """
    Replace emoji with the closest word in the review language
    """

    def __init__(self, language):
        self.analyser = SentimentIntensityAnalyzer()
        self.language = language
        self.emoji_set = set(UNICODE_EMOJI)
        self.format_space = ' {} '

    def emoji_sentiment_rating(self, emoji_char):
        return self.analyser.polarity_scores(emoji_char)['compound']

    def translate_class(self, word):
        if self.language == 'en':
            return word
        else:
            return SWEDISH_ENGLISH_TRANSLATE[word]

    def sentiment_rating_to_word(self, sentiment_rating):
        if sentiment_rating < 0.2:
            return self.translate_class(SENTIMENT_CLASSES[0])
        elif sentiment_rating < 0.5:
            return self.translate_class(SENTIMENT_CLASSES[1])
        else:
            return self.translate_class(SENTIMENT_CLASSES[2])


    def replace_emoji(self, word):
        list_chars = []
        for char in word:
            if char in self.emoji_set:
                sentiment_rating = self.emoji_sentiment_rating(char)
                sentiment_word = self.sentiment_rating_to_word(sentiment_rating)
                char = self.format_space.format(sentiment_word)
            list_chars.append(char)
        return ''.join(list_chars)


    def cleanup(self, content):
        return " ".join(self.replace_emoji(word) for word in content.split())



CONFIG = {
          'ucr': UnwantedCharsRemover,
          'stop': StopWordsRemover,
          'repeat': RepeatCharsRemover,
          'lemma': LemmaFormatter,
          'emoji': EmojiRemover
        }


class FiltersPipeline():
    def __init__(self, language, filters):
        self._filters_list = [CONFIG[filter.strip] for filter in filters.split(',')]

    def transform(self, content):
        for _filter in self._filters_list:
            content = _filter.cleanup(content)
        return content


def filter_contents(content, filters_pipeline, language=None):
    language = language if language else 'sv'
    pipeline = FiltersPipeline(language, filters_pipeline)
    return pipeline.transform(content)
