from MVC.Models.DatabaseOperationsModel import DatabaseOperationsModel

class ViewController:
    def __init__(self):
        # create an instance of DatabaseOperations to interact with the database
        self.database_operations = DatabaseOperationsModel()

    def check_if_user_exist(self, username, pwd):
        # check if the given username and password exist in the database
        r1, r2 = self.database_operations.authenticate_user(username, pwd)
        return r1, r2

    def add_user_to_database(self, username, pwd):
        # add a new user to the database with the given username and password
        result = self.database_operations.add_new_user(username, pwd)
        return result

    def add_history_to_database(self, username, recipe, link):
        # add a recipe to the user's search history in the database
        result = self.database_operations.add_history(username, recipe, link)
        return result

    def get_history_from_database(self, username):
        # retrieve the user's search history from the database
        result = self.database_operations.get_history(username)
        return result

    def add_favorite_recipe_to_database(self, username, recipe, link):
        # add a recipe to the user's favorite recipes in the database
        result = self.database_operations.add_favorite_recipe(username, recipe, link)
        return result

    def remove_favorite_recipe_from_database(self, username, recipe):
        # remove a recipe from the user's favorite recipes in the database
        result = self.database_operations.remove_favorite_recipe(username, recipe)
        return result

    def get_favorite_recipes_from_database(self, username):
        # retrieve the user's favorite recipes from the database
        result = self.database_operations.get_favorite_recipe(username)
        return result
