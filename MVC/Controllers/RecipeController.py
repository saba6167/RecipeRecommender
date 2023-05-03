from MVC.Models.RecipeModel import RecipeModel
from MVC.Controllers.IngredientsParserController import IngredientParserController
from sklearn.metrics.pairwise import cosine_similarity

class RecipeController:
    def __init__(self):
        # create an instance of RecipeModel
        self.recipe_model = RecipeModel()
        # load the trained Word2Vec model
        self.recipe_model.load_model(r'./MVC/Controllers/model_cbow.bin')
        # load the recipe data
        self.obj = IngredientParserController()
        self.recipe_model.load_data(r'./MVC/Controllers/df_parsed.csv')
        # parse the ingredients in the data using the IngredientParserController
        self.recipe_model.data['parsed'] =  self.recipe_model.data.ingredients.apply(self.obj.parse_ingredients)
        # preprocess and sort the ingredients in the data
        self.recipe_model.get_and_sort_corpus()
        # fit the model
        self.recipe_model.fit(method='tfidf')

    def get_recommendations(self, new_recipe, N=10):
        # parse the ingredients in the new recipe using the IngredientParserController
        new_recipe = new_recipe.split(",")
        new_recipe = self.obj.parse_ingredients(new_recipe)
        # get vector representation of new recipe
        new_recipe_vec = self.recipe_model.tfidf_vec_tr.do_transform([new_recipe])[0].reshape(1, -1)
        # calculate cosine similarity scores between new recipe and all recipes in data
        cos_sim = map(lambda x: cosine_similarity(new_recipe_vec, x)[0][0], self.recipe_model.doc_vec)
        # scores = cosine_similarity(new_recipe_vec, self.recipe_model.doc_vec)
        scores = list(cos_sim)
        # get top N recipe recommendations based on similarity scores
        recommendations = self.recipe_model.get_recommendations(N,scores)
        return recommendations