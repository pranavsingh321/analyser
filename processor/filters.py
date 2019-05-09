import re
from nltk.corpus import wordnet
from nltk.corpus import stopwords


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


class FiltersPipeline():
    def __init__(self, language, filters=None):
        self._filters_list = list()
        if filters is not None:
            self._filters_list += filters
        else:
            self._filters_list = [
                                  UnwantedCharsRemover,
                                  StopWordsRemover(language),
                                  RepeatCharsRemover(language)
                                 ]

    def filter(self, content):
        for _filter in self._filters:
            content = _filter.cleanup(content)
        return content


def filter_contents(content, language, filters_list=None):
    language = language if language else 'en'
    filter_pipeline = FiltersPipeline(filters_list, language)
    return filter_pipeline.filter(content)
