class RecipeVectorizer:
    def __init__(self, vectorizer):
        self.vectorizer = vectorizer

    def perform_fit(self,corpus):
        res = self.vectorizer.fit(corpus)
        return res
    def do_transform(self,docs):
        doc_word_vector = self.vectorizer.transform(docs)
        return doc_word_vector

