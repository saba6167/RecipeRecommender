from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from MVC.Models.Strategy.DefaultRecipeVectorizer import DefaultRecipeVectorizer

class TfidfEmbeddingVectorizer(DefaultRecipeVectorizer):
    def __init__(self, word_model):
        # Constructor to initialize the object with a given word_model
        self.word_model = word_model
        self.word_idf_weight = None
        self.vector_size = word_model.wv.vector_size

    def fit(self, docs):
        # Method to fit the model to the data and compute the IDF weights
        text_docs = []

        for doc in docs:
            text_docs.append(" ".join(doc))

        tfidf = TfidfVectorizer()
        tfidf.fit(text_docs)
        max_idf = max(tfidf.idf_)
        self.word_idf_weight = defaultdict(
            lambda: max_idf,
            [(word, tfidf.idf_[i]) for word, i in tfidf.vocabulary_.items()],
        )
        return self

    def transform(self, docs):
        # Method to transform the given documents using the TF-IDF weighted word embeddings
        doc_word_vector = self.word_average_list(docs)
        return doc_word_vector

    def word_average(self, sent):
        # Method to compute the TF-IDF weighted average word vector for a given sentence
        mean = []
        for word in sent:
            if word in self.word_model.wv.index_to_key:
                mean.append(
                    self.word_model.wv.get_vector(word) * self.word_idf_weight[word]
                )

        if not mean:
            return np.zeros(self.vector_size)
        else:
            mean = np.array(mean).mean(axis=0)
            return mean

    def word_average_list(self, docs):
        # Method to compute the TF-IDF weighted average word vectors for a list of sentences
        return np.vstack([self.word_average(sent) for sent in docs])