from RecipeRecommendationSystem import RecipeRecommenderSystem

if __name__ == '__main__':
    ##singleton
    # Creating a singleton instance of the Application class
    app = RecipeRecommenderSystem.get_instance()
    # Running the mainloop of the tkinter application
    app.root.mainloop()