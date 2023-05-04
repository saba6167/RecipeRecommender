from RecipeRecommender import RecipeRecommender

if __name__ == '__main__':
    # Singleton: The singleton pattern is a design pattern that restricts the instantiation of a class to a single
    # instance and ensures that there is only one instance of the class throughout the entire application.
    # The RecipeRecommender class is being implemented as a singleton using the get_instance() method.
    # By implementing the RecipeRecommender class as a singleton, we can ensure that only one instance
    # of the application is running at any given time, and that any attempts to create additional instances will
    # result in the same instance being returned.

    # Creating a singleton instance of the Application class
    app = RecipeRecommender.get_instance()
    # Running the mainloop of the tkinter application
    app.root.mainloop()