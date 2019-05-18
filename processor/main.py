def compose(*funcs):
    return lambda x: reduce(lambda f, g: g(f), list(funcs), x)

p = compose(foo1, foo2, foo3)
res = p(range(0, 5))


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords

from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()
nb.fit(X_train, y_train)


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

bow_transformer = CountVectorizer(analyzer=text_process).fit(X)

