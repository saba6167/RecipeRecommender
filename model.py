import sqlite3
import ast
import re
import string
from collections import defaultdict

import nltk
import numpy as np
import pandas as pd
import unidecode
from gensim.models import Word2Vec
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer


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
            self.mean_vec_tr = MeanEmbeddingVectorizer(self.model)
            self.doc_vec = self.mean_vec_tr.transform(self.corpus)
            self.doc_vec = [doc.reshape(1, -1) for doc in self.doc_vec]
            assert len(self.doc_vec) == len(self.corpus)
        else:
            self.tfidf_vec_tr = TfidfEmbeddingVectorizer(self.model)
            self.tfidf_vec_tr.fit(self.corpus)
            self.doc_vec = self.tfidf_vec_tr.transform(self.corpus)
            self.doc_vec = [doc.reshape(1, -1) for doc in self.doc_vec]
            assert len(self.doc_vec) == len(self.corpus)

    def get_recommendations(self, N, scores):
        df_recipes = pd.read_csv("df_parsed.csv")
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


class MeanEmbeddingVectorizer:
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

class TfidfEmbeddingVectorizer:
    def __init__(self, word_model):
        self.word_model = word_model
        self.word_idf_weight = None
        self.vector_size = word_model.wv.vector_size

    def fit(self, docs):
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
        doc_word_vector = self.word_average_list(docs)
        return doc_word_vector

    def word_average(self, sent):
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
        return np.vstack([self.word_average(sent) for sent in docs])

class IngredientParser:
    def __init__(self):
        self.measures = ['teaspoon', 't', 'tsp.', 'tablespoon', 'T', 'tbl.', 'tb', 'tbsp.', 'fluid ounce', 'fl oz', 'gill',
                'cup', 'c', 'pint', 'p', 'pt', 'fl pt', 'quart', 'q', 'qt', 'fl qt', 'gallon', 'g', 'gal', 'ml',
                'milliliter', 'millilitre', 'cc', 'mL', 'l', 'liter', 'litre', 'L', 'dl', 'deciliter', 'decilitre',
                'dL', 'bulb', 'level', 'heaped', 'rounded', 'whole', 'pinch', 'medium', 'slice', 'pound', 'lb', '#',
                'ounce', 'oz', 'mg', 'milligram', 'milligramme', 'g', 'gram', 'gramme', 'kg', 'kilogram', 'kilogramme',
                'x', 'of', 'mm', 'millimetre', 'millimeter', 'cm', 'centimeter', 'centimetre', 'm', 'meter', 'metre',
                'inch', 'in', 'milli', 'centi', 'deci', 'hecto', 'kilo']
        self.words_to_remove = ['fresh', 'oil', 'a', 'red', 'bunch', 'and', 'clove', 'or', 'leaf', 'chilli', 'large', 'extra',
                       'sprig', 'ground', 'handful', 'free', 'small', 'pepper', 'virgin', 'range', 'from', 'dried',
                       'sustainable', 'black', 'peeled', 'higher', 'welfare', 'seed', 'for', 'finely', 'freshly', 'sea',
                       'quality', 'white', 'ripe', 'few', 'piece', 'source', 'to', 'organic', 'flat', 'smoked',
                       'ginger', 'sliced', 'green', 'picked', 'the', 'stick', 'plain', 'plus', 'mixed', 'mint', 'bay',
                       'basil', 'your', 'cumin', 'optional', 'fennel', 'serve', 'mustard', 'unsalted', 'baby',
                       'paprika', 'fat', 'ask', 'natural', 'skin', 'roughly', 'into', 'such', 'cut', 'good', 'brown',
                       'grated', 'trimmed', 'oregano', 'powder', 'yellow', 'dusting', 'knob', 'frozen', 'on',
                       'deseeded', 'low', 'runny', 'balsamic', 'cooked', 'streaky', 'nutmeg', 'sage', 'rasher', 'zest',
                       'pin', 'groundnut', 'breadcrumb', 'turmeric', 'halved', 'grating', 'stalk', 'light', 'tinned',
                       'dry', 'soft', 'rocket', 'bone', 'colour', 'washed', 'skinless', 'leftover', 'splash', 'removed',
                       'dijon', 'thick', 'big', 'hot', 'drained', 'sized', 'chestnut', 'watercress', 'fishmonger',
                       'english', 'dill', 'caper', 'raw', 'worcestershire', 'flake', 'cider', 'cayenne', 'tbsp', 'leg',
                       'pine', 'wild', 'if', 'fine', 'herb', 'almond', 'shoulder', 'cube', 'dressing', 'with', 'chunk',
                       'spice', 'thumb', 'garam', 'new', 'little', 'punnet', 'peppercorn', 'shelled', 'saffron',
                       'other''chopped', 'salt', 'olive', 'taste', 'can', 'sauce', 'water', 'diced', 'package',
                       'italian', 'shredded', 'divided', 'parsley', 'vinegar', 'all', 'purpose', 'crushed', 'juice',
                       'more', 'coriander', 'bell', 'needed', 'thinly', 'boneless', 'half', 'thyme', 'cubed',
                       'cinnamon', 'cilantro', 'jar', 'seasoning', 'rosemary', 'extract', 'sweet', 'baking', 'beaten',
                       'heavy', 'seeded', 'tin', 'vanilla', 'uncooked', 'crumb', 'style', 'thin', 'nut', 'coarsely',
                       'spring', 'chili', 'cornstarch', 'strip', 'cardamom', 'rinsed', 'honey', 'cherry', 'root',
                       'quartered', 'head', 'softened', 'container', 'crumbled', 'frying', 'lean', 'cooking', 'roasted',
                       'warm', 'whipping', 'thawed', 'corn', 'pitted', 'sun', 'kosher', 'bite', 'toasted', 'lasagna',
                       'split', 'melted', 'degree', 'lengthwise', 'romano', 'packed', 'pod', 'anchovy', 'rom',
                       'prepared', 'juiced', 'fluid', 'floret', 'room', 'active', 'seasoned', 'mix', 'deveined',
                       'lightly', 'anise', 'thai', 'size', 'unsweetened', 'torn', 'wedge', 'sour', 'basmati',
                       'marinara', 'dark', 'temperature', 'garnish', 'bouillon', 'loaf', 'shell', 'reggiano', 'canola',
                       'parmigiano', 'round', 'canned', 'ghee', 'crust', 'long', 'broken', 'ketchup', 'bulk', 'cleaned',
                       'condensed', 'sherry', 'provolone', 'cold', 'soda', 'cottage', 'spray', 'tamarind', 'pecorino',
                       'shortening', 'part', 'bottle', 'sodium', 'cocoa', 'grain', 'french', 'roast', 'stem', 'link',
                       'firm', 'asafoetida', 'mild', 'dash', 'boiling']
        self.translator = str.maketrans('', '', string.punctuation)
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(nltk.corpus.stopwords.words('english'))

    def parse(self, ingredients):
        if isinstance(ingredients, list):
            ingredients = ingredients
        else:
            ingredients = ast.literal_eval(ingredients)

        ingred_list = []
        for i in ingredients:
            i.translate(self.translator)
            items = re.split(' |-', i)
            items = [word for word in items if word.isalpha()]
            items = [word.lower() for word in items]
            items = [unidecode.unidecode(word) for word in items]
            items = [self.lemmatizer.lemmatize(word) for word in items]
            items = [word for word in items if word not in self.stop_words]
            items = [word for word in items if word not in self.measures]
            items = [word for word in items if word not in self.words_to_remove]
            if items:
                ingred_list.append(' '.join(items))
        return ingred_list

class DatabaseOperations:
    def authenticate_user(self, username, password):
        with sqlite3.connect('RecipeRecommender.db') as db:
            c = db.cursor()
            query1 = 'SELECT * FROM user WHERE username = ? and password = ?'
            c.execute(query1, [(username), (password)])
            pass_correct = c.fetchall()
            query2 = 'SELECT * FROM user WHERE username = ?'
            c.execute(query2, [(username)])
            user_exist = c.fetchall()
            return user_exist,pass_correct

    def add_new_user(self,username,pwd):
        with sqlite3.connect('RecipeRecommender.db') as db:
            c = db.cursor()
            find_user = ('SELECT username FROM user WHERE username = ?')
            c.execute(find_user, [(username)])
            rows = c.fetchall()
            print(rows)
            if not rows:
                print("Inserted")
                insert = 'INSERT INTO user(username,password) VALUES(?,?)'
                c.execute(insert, [(username), (pwd)])
                db.commit()
            else:
                print(rows)
                return rows
    def add_history(self,username,recipe,link):
        with sqlite3.connect('RecipeRecommender.db') as db:
            print("connected")
            c = db.cursor()
            find_user = ('SELECT username FROM userhistory WHERE recipe = ? AND username = ?')
            c.execute(find_user, [(recipe),(username)])
            if c.fetchall():
                return True
            else:
                insert = 'INSERT INTO userhistory(username,recipe,link) VALUES(?,?,?)'
                c.execute(insert, [(username), (recipe), (link)])
                db.commit()
                return True

    def get_history(self,username):
        with sqlite3.connect('RecipeRecommender.db') as db:
            c = db.cursor()
            find_user = ('SELECT recipe,link FROM userhistory WHERE username = ?')
            c.execute(find_user, (username,))
            rows = c.fetchall()
            if rows:
                return rows

    def add_favorite_recipe(self,username,recipe,link):
        with sqlite3.connect('RecipeRecommender.db') as db:
            print("connected")
            c = db.cursor()
            find_user = ('SELECT username FROM favoriterecipes WHERE recipe = ? AND username = ?')
            c.execute(find_user, [(recipe),(username)])
            if c.fetchall():
                return True
            else:
                insert = 'INSERT INTO favoriterecipes(username,recipe,link) VALUES(?,?,?)'
                c.execute(insert, [(username), (recipe), (link)])
                db.commit()
                return True

    def remove_favorite_recipe(self,username,recipe):
        with sqlite3.connect('RecipeRecommender.db') as db:
            print("connected")
            c = db.cursor()
            find_user = ('DELETE FROM favoriterecipes WHERE username = ? AND recipe = ?')
            res = c.execute(find_user, [(username),(recipe)])
            if res:
                return True
            else:
                return False

    def get_favorite_recipe(self,username):
        with sqlite3.connect('RecipeRecommender.db') as db:
            c = db.cursor()
            find_user = ('SELECT recipe,link FROM favoriterecipes WHERE username = ?')
            c.execute(find_user, (username,))
            rows = c.fetchall()
            if rows:
                return rows