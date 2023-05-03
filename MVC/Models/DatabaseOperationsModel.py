import sqlite3

class DatabaseOperations:
    # Method to authenticate a user with a given username and password
    def authenticate_user(self, username, password):
        with sqlite3.connect('RecipeRecommender.db') as db:
            c = db.cursor()
            query1 = 'SELECT * FROM user WHERE username = ? and password = ?'
            c.execute(query1, [(username), (password)])
            pass_correct = c.fetchall()
            query2 = 'SELECT * FROM user WHERE username = ?'
            c.execute(query2, [(username)])
            user_exist = c.fetchall()
            return user_exist, pass_correct

    # Method to add a new user with a given username and password
    def add_new_user(self, username, pwd):
        with sqlite3.connect('RecipeRecommender.db') as db:
            c = db.cursor()
            find_user = ('SELECT username FROM user WHERE username = ?')
            c.execute(find_user, [(username)])
            rows = c.fetchall()
            print(rows)
            if not rows:
                print("Inserted")
                insert = 'INSERT INTO user(username,password) VALUES(?,?)'
                c.execute(insert, [(username), (pwd)])
                db.commit()
            else:
                print(rows)
                return rows

    def add_history(self, username, recipe, link):
        with sqlite3.connect('RecipeRecommender.db') as db:
            # Connect to the database
            c = db.cursor()
            # Check if the recipe already exists in the user's history
            find_user = ('SELECT username FROM userhistory WHERE recipe = ? AND username = ?')
            c.execute(find_user, [(recipe), (username)])
            if c.fetchall():
                # If the recipe already exists, return True
                return True
            else:
                # Otherwise, add the recipe to the user's history table
                insert = 'INSERT INTO userhistory(username,recipe,link) VALUES(?,?,?)'
                c.execute(insert, [(username), (recipe), (link)])
                db.commit()
                # Return True to indicate successful addition
                return True

    def get_history(self, username):
        with sqlite3.connect('RecipeRecommender.db') as db:
            # Connect to the database
            c = db.cursor()
            # Get all the recipes in the user's history
            find_user = ('SELECT recipe,link FROM userhistory WHERE username = ?')
            c.execute(find_user, (username,))
            rows = c.fetchall()
            if rows:
                # If there are any recipes in the user's history, return them
                return rows

    def add_favorite_recipe(self, username, recipe, link):
        with sqlite3.connect('RecipeRecommender.db') as db:
            # Connect to the database
            c = db.cursor()
            # Check if the recipe already exists in the user's favorite recipes
            find_user = ('SELECT username FROM favoriterecipes WHERE recipe = ? AND username = ?')
            c.execute(find_user, [(recipe), (username)])
            if c.fetchall():
                # If the recipe already exists, return True
                return True
            else:
                # Otherwise, add the recipe to the user's favorite recipes table
                insert = 'INSERT INTO favoriterecipes(username,recipe,link) VALUES(?,?,?)'
                c.execute(insert, [(username), (recipe), (link)])
                db.commit()
                # Return True to indicate successful addition
                return True

    def remove_favorite_recipe(self, username, recipe):
        with sqlite3.connect('RecipeRecommender.db') as db:
            # connect to database
            print("connected")
            c = db.cursor()
            # delete the row with the given username and recipe
            find_user = ('DELETE FROM favoriterecipes WHERE username = ? AND recipe = ?')
            res = c.execute(find_user, [(username), (recipe)])
            if res:
                # if the row is deleted, return True
                return True
            else:
                # if the row is not deleted, return False
                return False

    def get_favorite_recipe(self, username):
        with sqlite3.connect('RecipeRecommender.db') as db:
            c = db.cursor()
            # get all the rows with the given username
            find_user = ('SELECT recipe,link FROM favoriterecipes WHERE username = ?')
            c.execute(find_user, (username,))
            rows = c.fetchall()
            if rows:
                # if there are any rows, return them
                return rows