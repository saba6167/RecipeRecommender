from Observer.Observer import Observer

class RecipeHistory(Observer):
    def update(self,controller, name,recipe,link):
        # Method to update the recipe history with the latest recipe added by the user
        controller.add_history_to_database(name,recipe, link)