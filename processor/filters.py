import re
from nltk.corpus import wordnet
from nltk.corpus import stopwords


class StopWordsRemover():

    def __init__(self, text, language):
        self.stopwords = set(stopwords.words(language))
        self.text = text

    def __call__(self):
        return self.cleanup()

    def cleanup(self):
        return " ".join(word for word in self.text.split() \
                       if word not in self.stopwords)


class UnwantedCharsRemover():

    def __init__(self, text, language):
        self.text = text
        self.unwanted_chars = '?.,!:;"$%^&*()#@+/<>=\\[]_~{}|`'

    def __call__(self):
        return self.cleanup()

    def cleanup(self):
        return self.text.translate({ord(c): None for c in self.unwanted_chars})


class RepeatCharsRemover():

    def __init__(self, text, language):
        self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'
        self.text = text
        self.language = language

    def __call__(self):
        return self.cleanup()

    def cleanup(self):
        return " ".join(self.replace_remover(word) for word in self.text.split())

    def replace_remover(self, word):
        if wordnet.synsets(word, lang=self.language):
            return word
        repl_word = self.repeat_regexp.sub(self.repl, word)
        if repl_word != word:
            return self.replace(repl_word)
        else:
            return repl_word


class FiltersPipeline(object):
    def __init__(self, filters=None):
        self._filters = list()
        if filters is not None:
            self._filters += filters

    def filter(self, content):
        for filter in self._filters:
            content = filter(content)
        return content


def filter_contents(content, language, filters_list=None):
    if not filters_list:
        filters_list = [UnwantedCharsRemover, StopWordsRemover, RepeatCharsRemover]
    filter = FiltersPipeline(filters_list)
    return filter.filter(content, language)
