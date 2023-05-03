from RecipeRecommendationSystem import Application

if __name__ == '__main__':
    ##singleton
    # Creating a singleton instance of the Application class
    app = Application.get_instance()
    # Running the mainloop of the tkinter application
    app.root.mainloop()