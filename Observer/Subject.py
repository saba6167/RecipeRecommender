class Subject:
    # Observer: The observer pattern is used when one object needs to notify one or more other objects of any changes
    # to its state. The subject maintains a list of observers and notifies them of any changes to its state.
    # RecipeObserver is the subject that maintains a list of observers, while RecipeHistory is an observer that is
    # notified of any changes in state. The RecipeObserver class has three methods: attach, detach, and notify, while
    # the Observer class defines the update method. Overall, the observer pattern is being used to decouple the
    # RecipeObserver and RecipeHistory classes, making the code more modular and easier to maintain.
    def attach(self, observer):
        # Method to attach an observer to the subject
        pass

    def detach(self, observer):
        # Method to detach an observer from the subject
        pass

    def notify(self):
        # Method to notify all the observers about the change in the state of the subject
        pass
