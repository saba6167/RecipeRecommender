# This class provides a wrapper for a vectorizer to use with recipe text data.

class RecipeVectorizer:
    # Strategy: The code uses the Strategy design pattern to implement different vectorization strategies for the
    # RecipeModel class. The RecipeVectorizer class is the strategy interface, and the TfidfEmbeddingVectorizerModel
    # and MeanEmbeddingVectorizerModel classes are concrete strategy implementations. The RecipeVectorizer class has
    # two methods: perform_fit and do_transform, which take a vectorizer as input and fit and transform the corpus
    # into document vectors, respectively. The TfidfEmbeddingVectorizerModel and MeanEmbeddingVectorizerModel classes
    # implement the fit method of the vectorizer, which fits the vectorizer to the provided corpus and returns the
    # fitted vectorizer. The RecipeModel class uses the RecipeVectorizer class to transform the corpus into document
    # vectors.
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
