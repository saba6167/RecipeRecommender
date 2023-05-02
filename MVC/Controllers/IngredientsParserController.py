from MVC.Models.IngredientParserModel import IngredientParser

class IngredientParserController:
    def __init__(self):
        self.ingredient_parser = IngredientParser()

    def parse_ingredients(self, ingredients):
        return self.ingredient_parser.parse(ingredients)