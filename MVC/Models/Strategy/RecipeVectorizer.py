# This class provides a wrapper for a vectorizer to use with recipe text data.

class RecipeVectorizer:

    def __init__(self, vectorizer):
        # Constructor to initialize the RecipeVectorizer instance.
        # It takes a vectorizer as input parameter.
        self.vectorizer = vectorizer

    def perform_fit(self, corpus):
        # This method fits the vectorizer to the provided corpus.
        # It takes the corpus as input parameter.
        # It returns the fitted vectorizer.
        res = self.vectorizer.fit(corpus)
        return res

    def do_transform(self, docs):
        # This method applies the fitted vectorizer to the provided documents and returns the document-word vectors.
        # It takes the documents as input parameter.
        doc_word_vector = self.vectorizer.transform(docs)
        return doc_word_vector
