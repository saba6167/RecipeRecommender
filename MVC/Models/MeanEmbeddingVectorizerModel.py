import numpy as np
from MVC.Models.Strategy.DefaultRecipeVectorizer import DefaultRecipeVectorizer


class MeanEmbeddingVectorizer(DefaultRecipeVectorizer):
    def __init__(self, word_model):
        self.word_model = word_model
        self.vector_size = word_model.wv.vector_size

    def fit(self):
        return self

    def transform(self, docs):
        doc_word_vector = self.word_average_list(docs)
        return doc_word_vector

    def word_average(self, sent):
        mean = []
        for word in sent:
            if word in self.word_model.wv.index_to_key:
                mean.append(self.word_model.wv.get_vector(word))

        if not mean:  # empty words
            return np.zeros(self.vector_size)
        else:
            mean = np.array(mean).mean(axis=0)
            return mean

    def word_average_list(self, docs):
        return np.vstack([self.word_average(sent) for sent in docs])