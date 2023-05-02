import sqlite3
import ast
import pandas as pd
import unidecode
from gensim.models import Word2Vec
from MVC.Models.TfidfEmbeddingVectorizerModel import TfidfEmbeddingVectorizer
from MVC.Models.MeanEmbeddingVectorizerModel import MeanEmbeddingVectorizer
from MVC.Models.Strategy.RecipeVectorizer import RecipeVectorizer

class RecipeModel:
    def __init__(self):
        self.db = sqlite3.connect('RecipeRecommender.db')
        self.cursor = self.db.cursor()
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL PRIMARY KEY,password TEXT NOT NULL);')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS userhistory (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL,recipe TEXT NOT NULL,link TEXT NOT NULL);')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS favoriterecipes (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL,recipe TEXT NOT NULL,link TEXT NOT NULL);')
        self.db.commit()
        self.success_user_name = ''
        self.model = None
        self.mean_vec_tr = None
        self.tfidf_vec_tr = None
        self.data = None
        self.corpus = None
        self.doc_vec = None

    def load_model(self, model_path):
        self.model = Word2Vec.load(model_path)
        self.model.init_sims(replace=True)
        if self.model:
            print("Successfully loaded model")

    def load_data(self, data_path):
        self.data = pd.read_csv(data_path)
        self.data["parsed"] = self.data.ingredients.apply(self.ingredient_parser)

    def ingredient_parser(self, ingredient):
        if isinstance(ingredient, list):
            ingredients = ingredient
        else:
            ingredients = ast.literal_eval(ingredient)

        ingredients = ",".join(ingredients)
        ingredients = unidecode.unidecode(ingredients)
        return ingredients

    def get_and_sort_corpus(self):
        corpus_sorted = []
        for doc in self.data.parsed.values:
            doc.sort()
            corpus_sorted.append(doc)
        self.corpus = corpus_sorted

    def fit(self, method="tfidf"):
        if method == "mean":
            self.mean_vec_tr = RecipeVectorizer(MeanEmbeddingVectorizer(self.model))
            self.doc_vec = self.mean_vec_tr.do_transform(self.corpus)
            self.doc_vec = [doc.reshape(1, -1) for doc in self.doc_vec]
            assert len(self.doc_vec) == len(self.corpus)
        else:
            self.tfidf_vec_tr = RecipeVectorizer(TfidfEmbeddingVectorizer(self.model))
            self.tfidf_vec_tr.perform_fit(self.corpus)
            self.doc_vec = self.tfidf_vec_tr.do_transform(self.corpus)
            self.doc_vec = [doc.reshape(1, -1) for doc in self.doc_vec]
            assert len(self.doc_vec) == len(self.corpus)

    def get_recommendations(self, N, scores):
        df_recipes = pd.read_csv(r"C:\Users\mehmo\AppData\Roaming\JetBrains\PyCharmCE2022.2\scratches\RecipeRecommendationSystem_V1\MVC\Controllers\df_parsed.csv")
        top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:N]
        recommendation = pd.DataFrame(columns=["recipe", "ingredients", "score", "url"])
        count = 0
        for i in top:
            recommendation.at[count, "recipe"] = self.title_parser(df_recipes["recipe_name"][i])
            recommendation.at[count, "ingredients"] = self.ingredient_parser_final(
                df_recipes["ingredients"][i]
            )
            recommendation.at[count, "url"] = df_recipes["recipe_urls"][i]
            recommendation.at[count, "score"] = f"{scores[i]}"
            count += 1
        return recommendation

    def title_parser(self, title):
        return unidecode.unidecode(title)

    def ingredient_parser_final(self, ingredient):
        ingredients = self.ingredient_parser(ingredient)
        return ingredients