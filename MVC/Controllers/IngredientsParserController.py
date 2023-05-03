from MVC.Models.IngredientParserModel import IngredientParserModel

class IngredientParserController:
    def __init__(self):
        # Initializes an instance of the IngredientParser class
        self.ingredient_parser = IngredientParserModel()

    def parse_ingredients(self, ingredients):
        # Calls the parse method of the IngredientParser instance and passes the ingredients string as argument
        # Returns the parsed ingredients as a list
        return self.ingredient_parser.parse(ingredients)