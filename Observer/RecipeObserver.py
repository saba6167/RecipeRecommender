from Observer.Subject import Subject

class RecipeObserver(Subject):
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self,controller,name,recipe,link):
        for observer in self.observers:
            res = observer.update(controller,name,recipe,link)
            return res