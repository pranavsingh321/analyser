class LDAFeatureExtract:
    """
    Extract the features in the text passed.
    Basically do the keyword analysis based on popular algo LDA.
    """

    def __init__(self, text, language):
        self.text_tokens = text.lower().split()
        self.language = language
        self.dictionary = corpora.Dictionary(self.text_tokens)
        self.freq_corpus = None

    def _preprocessing(self,):
        '''
        Create the preprocessing, create freq dicttionary, corpus
        '''
        # text to id
        self.dictionary.filter_extremes(no_below=2, no_above=0.7, keep_n=100000)

        # convert tokenized documents into a document-term matrix
        if not self.freq_corpus:
            self.freq_corpus = [self.dictionary.doc2bow(text)
                                for text in self.text_tokens]

    def create_bigrams_trigrams(self, min_count=5, trigram=True):
        """
          Bigram, Trigram creation
        """
        # higher threshold fewer phrases.
        bigram = gensim.models.Phrases(self.text_tokens, min_count=min_count, threshold=100)
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        bigram_data = [bigram_mod[doc] for doc in self.text_tokens],

        if trigram:
            trigram = gensim.models.Phrases(bigram[self.text_tokens], threshold=100)
            trigram_mod = gensim.models.phrases.Phraser(trigram)
            trigram_data = [trigram_mod[bigram_mod[doc]] for doc in self.text_tokens]
            return bigram_data, trigram_data

        return bigram_data

    def process_LDA(self, num_topics=10):
        """
        Do the LDA based feature extraction
        """
        self._preprocessing()
        # lda_model = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics,
        #                                               id2word = dictionary,
        #                                               passes=15)
        lda_model = gensim.models.LdaMulticore(self.freq_corpus,
                                               num_topics=num_topics,
                                               id2word=self.dictionary,
                                               passes=15, workers=2)
        return lda_model

    def process_TFIDF(self, num_topics=10, return_corpus=False):
        """
        Do the TFIDF based feature extraction
        """
        self._preprocessing()
        tfidf = models.TfidfModel(self.freq_corpus)
        if return_corpus:
            _corpus_tfidf = tfidf[self.freq_corpus]
            return tfidf, _corpus_tfidf

        return tfidf

    def LDA_ON_TFIDF(self, num_topics=10):
        """
        Apply the LDA on TF-IDF corpus
        """
        _tfidf, corpus_tfidf = self.process_TFIDF(return_corpus=True)
        lda_on_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=num_topics,
                                                  id2word=self.dictionary,
                                                  passes=4, workers=4)
        return lda_on_tfidf

