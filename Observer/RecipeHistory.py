from Observer.Observer import Observer

class RecipeHistory(Observer):
    def update(self,controller, name,recipe,link):
        res = controller.add_history_to_database(name,recipe, link)