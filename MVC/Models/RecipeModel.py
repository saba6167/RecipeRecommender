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
        # Connect to the SQLite database
        self.db = sqlite3.connect('RecipeRecommender.db')
        self.cursor = self.db.cursor()
        # Create tables for user, userhistory and favoriterecipes if they don't exist
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
        # Load the Word2Vec model and initialize it
        self.model = Word2Vec.load(model_path)
        self.model.init_sims(replace=True)

        # If the model is successfully loaded, print a message
        if self.model:
            print("Successfully loaded model")

    def load_data(self, data_path):
        # Read the recipe data from the given csv file
        self.data = pd.read_csv(data_path)

        # Parse the 'ingredients' column of the data using the ingredient_parser function
        self.data["parsed"] = self.data.ingredients.apply(self.ingredient_parser)

    def ingredient_parser(self, ingredient):
        # Check if the ingredient is a list
        if isinstance(ingredient, list):
            ingredients = ingredient
        else:
            # If the ingredient is not a list, evaluate it as a literal expression and convert to a list
            ingredients = ast.literal_eval(ingredient)

        # Join the ingredients with commas and remove any accents from the text
        ingredients = ",".join(ingredients)
        ingredients = unidecode.unidecode(ingredients)

        # Return the parsed ingredients
        return ingredients

    def get_and_sort_corpus(self):
        # Sort and preprocess corpus by sorting ingredients alphabetically
        corpus_sorted = []
        for doc in self.data.parsed.values:
            doc.sort()
            corpus_sorted.append(doc)
        self.corpus = corpus_sorted

    def fit(self, method="tfidf"):
        if method == "mean":
            # Use the mean embedding vectorizer to transform the corpus into document vectors
            self.mean_vec_tr = RecipeVectorizer(MeanEmbeddingVectorizer(self.model))
            self.doc_vec = self.mean_vec_tr.do_transform(self.corpus)
            self.doc_vec = [doc.reshape(1, -1) for doc in self.doc_vec]
            assert len(self.doc_vec) == len(self.corpus)
        else:
            # Use the TF-IDF embedding vectorizer to transform the corpus into document vectors
            self.tfidf_vec_tr = RecipeVectorizer(TfidfEmbeddingVectorizer(self.model))
            self.tfidf_vec_tr.perform_fit(self.corpus)
            self.doc_vec = self.tfidf_vec_tr.do_transform(self.corpus)
            self.doc_vec = [doc.reshape(1, -1) for doc in self.doc_vec]
            assert len(self.doc_vec) == len(self.corpus)

    def get_recommendations(self, N, scores):
        # Retrieve top N recommended recipes and their details from the preprocessed corpus
        df_recipes = pd.read_csv(r"./MVC/Controllers/df_parsed.csv")
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
        # Clean recipe titles by converting special characters to ASCII format
        return unidecode.unidecode(title)

    def ingredient_parser_final(self, ingredient):
        # Preprocess ingredient lists by sorting them alphabetically and removing special characters
        ingredients = self.ingredient_parser(ingredient)
        return ingredients