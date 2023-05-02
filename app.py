from RecipeRecommendationSystem import Application


if __name__ == '__main__':
    ##singleton
    app = Application.get_instance()
    app.root.mainloop()