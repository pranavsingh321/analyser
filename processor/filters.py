import re
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from emoji import UNICODE_EMOJI


SENTIMENT_CLASSES = ('bad', 'ok', 'good')
SWEDISH_ENGLISH_TRANSLATE = {SENTIMENT_CLASSES[0]:'dålig', SENTIMENT_CLASSES[1]:'ok', SENTIMENT_CLASSES[2]:'Bra'}


class StopWordsRemover():

    def __init__(self, language):
        self.stopwords = set(stopwords.words(language))

    def cleanup(self, content):
        return " ".join(word for word in content.split()
                        if word not in self.stopwords)


class UnwantedCharsRemover():

    def __init__(self):
        self.unwanted_chars = '?.,!:;"$%^&*()#@+/<>=\\[]_~{}|`'

    def cleanup(self, content):
        return content.translate({ord(c): None for c in self.unwanted_chars})


class RepeatCharsRemover():

    def __init__(self, text, language):
        self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'
        self.text = text
        self.language = language

    def cleanup(self):
        return " ".join(self.replace_remover(word)
                        for word in self.text.split())

    def replace_remover(self, word):
        if wordnet.synsets(word, lang=self.language):
            return word
        repl_word = self.repeat_regexp.sub(self.repl, word)
        if repl_word != word:
            return self.replace(repl_word)
        else:
            return repl_word


class EmojiRemover():

    def __init__(self, language):
        self.analyser = SentimentIntensityAnalyzer()
        self.language = language
        self.emoji_set = set(UNICODE_EMOJI)
        self.format_space = ' {} '

    def emoji_sentiment_rating(self, emoji_char):
        return analyser.polarity_scores(sentence)['compound']

    def translate_class(self, word):
        if self.language == 'en':
            return word
        else:
            return SWEDISH_ENGLISH_TRANSLATE[word]

    def sentiment_rating_to_word(self, sentiment_rating):
        if sentiment < 0.2:
            return self.translate_class(SENTIMENT_CLASSES[0])
        elif sentiment < 0.5:
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
        return " ".join(replace_emoji(word) for word in content.split())


class FiltersPipeline():
    def __init__(self, language, filters=None):
        self._filters_list = list()
        if filters is not None:
            self._filters_list += filters
        else:
            self._filters_list = [
                                  UnwantedCharsRemover,
                                  StopWordsRemover(language),
                                  RepeatCharsRemover(language),
                                  EmojiRemover(language)
                                 ]

    def filter(self, content):
        for _filter in self._filters:
            content = _filter.cleanup(content)
        return content


def filter_contents(content, language, filters_list=None):
    language = language if language else 'en'
    filter_pipeline = FiltersPipeline(filters_list, language)
    return filter_pipeline.filter(content)
