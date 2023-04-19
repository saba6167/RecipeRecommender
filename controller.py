from model import RecipeModel
from model import IngredientParser
from model import DatabaseOperations
from sklearn.metrics.pairwise import cosine_similarity

class RecipeController:
    def __init__(self):
        # create an instance of RecipeModel
        self.recipe_model = RecipeModel()
        # load the trained Word2Vec model
        self.recipe_model.load_model('model_cbow.bin')
        # load the recipe data
        self.obj = IngredientParserController()
        self.recipe_model.load_data('df_parsed.csv')
        self.recipe_model.data['parsed'] =  self.recipe_model.data.ingredients.apply(self.obj.parse_ingredients)
        # preprocess and sort the ingredients in the data
        self.recipe_model.get_and_sort_corpus()
        # fit the model
        self.recipe_model.fit(method='tfidf')

    def get_recommendations(self, new_recipe, N=5):
        new_recipe = new_recipe.split(",")
        new_recipe = self.obj.parse_ingredients(new_recipe)
        # get vector representation of new recipe
        new_recipe_vec = self.recipe_model.tfidf_vec_tr.transform([new_recipe])[0].reshape(1, -1)
        # calculate cosine similarity scores between new recipe and all recipes in data
        cos_sim = map(lambda x: cosine_similarity(new_recipe_vec, x)[0][0], self.recipe_model.doc_vec)
        # scores = cosine_similarity(new_recipe_vec, self.recipe_model.doc_vec)
        scores = list(cos_sim)
        # get top N recipe recommendations based on similarity scores
        recommendations = self.recipe_model.get_recommendations(N,scores)
        return recommendations

class IngredientParserController:
    def __init__(self):
        self.ingredient_parser = IngredientParser()

    def parse_ingredients(self, ingredients):
        return self.ingredient_parser.parse(ingredients)


class ViewController:
    def __init__(self):
        self.database_operations = DatabaseOperations()

    def check_if_user_exist(self,username,pwd):
        r1,r2 = self.database_operations.authenticate_user(username,pwd)
        return r1,r2

    def add_user_to_database(self,username,pwd):
        result = self.database_operations.add_new_user(username,pwd)
        return result

    def add_history_to_database(self,username,recipe,link):
        result = self.database_operations.add_history(username, recipe,link)
        return result

    def get_history_from_database(self,username):
        result = self.database_operations.get_history(username)
        return result

    def add_favorite_recipe_to_database(self,username,recipe,link):
        result = self.database_operations.add_favorite_recipe(username,recipe,link)
        return result

    def remove_favorite_recipe_from_database(self,username, recipe):
        result = self.database_operations.remove_favorite_recipe(username, recipe)
        return result
    def get_favorite_recipes_from_database(self,username):
        result = self.database_operations.get_favorite_recipe(username)
        return result