from MVC.Models.DatabaseOperationsModel import DatabaseOperations

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