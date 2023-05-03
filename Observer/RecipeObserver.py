from Observer.Subject import Subject

class RecipeObserver(Subject):
    def __init__(self):
        # Constructor to initialize the observers list
        self.observers = []

    def attach(self, observer):
        # Method to attach an observer to the observer list
        self.observers.append(observer)

    def detach(self, observer):
        # Method to detach an observer from the observer list
        self.observers.remove(observer)

    def notify(self, controller, name, recipe, link):
        # Method to notify all the observers about the change in the state of the subject
        for observer in self.observers:
            res = observer.update(controller, name, recipe, link)
            return res
