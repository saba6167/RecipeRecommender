import numpy as np
from MVC.Models.Strategy.DefaultRecipeVectorizer import DefaultRecipeVectorizer

class MeanEmbeddingVectorizerModel(DefaultRecipeVectorizer):
    # Polymorphism: The MeanEmbeddingVectorizerModel class defines its own implementation of the fit() and
    # transform() methods, which are also defined in the parent class DefaultRecipeVectorizer
    def __init__(self, word_model):
        # Constructor to initialize the object with a given word_model
        self.word_model = word_model
        self.vector_size = word_model.wv.vector_size

    def fit(self):
        # Method to fit the model to the data
        return self

    def transform(self, docs):
        # Method to transform the given documents using the word embeddings
        doc_word_vector = self.word_average_list(docs)
        return doc_word_vector

    def word_average(self, sent):
        # Method to compute the average word vector for a given sentence
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
        # Method to compute the average word vectors for a list of sentences
        return np.vstack([self.word_average(sent) for sent in docs])
