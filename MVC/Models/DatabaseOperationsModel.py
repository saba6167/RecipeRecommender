import sqlite3

class DatabaseOperations:
    def authenticate_user(self, username, password):
        with sqlite3.connect('RecipeRecommender.db') as db:
            c = db.cursor()
            query1 = 'SELECT * FROM user WHERE username = ? and password = ?'
            c.execute(query1, [(username), (password)])
            pass_correct = c.fetchall()
            query2 = 'SELECT * FROM user WHERE username = ?'
            c.execute(query2, [(username)])
            user_exist = c.fetchall()
            return user_exist,pass_correct

    def add_new_user(self,username,pwd):
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
    def add_history(self,username,recipe,link):
        with sqlite3.connect('RecipeRecommender.db') as db:
            print("connected")
            c = db.cursor()
            find_user = ('SELECT username FROM userhistory WHERE recipe = ? AND username = ?')
            c.execute(find_user, [(recipe),(username)])
            if c.fetchall():
                return True
            else:
                insert = 'INSERT INTO userhistory(username,recipe,link) VALUES(?,?,?)'
                c.execute(insert, [(username), (recipe), (link)])
                db.commit()
                return True

    def get_history(self,username):
        with sqlite3.connect('RecipeRecommender.db') as db:
            c = db.cursor()
            find_user = ('SELECT recipe,link FROM userhistory WHERE username = ?')
            c.execute(find_user, (username,))
            rows = c.fetchall()
            if rows:
                return rows

    def add_favorite_recipe(self,username,recipe,link):
        with sqlite3.connect('RecipeRecommender.db') as db:
            print("connected")
            c = db.cursor()
            find_user = ('SELECT username FROM favoriterecipes WHERE recipe = ? AND username = ?')
            c.execute(find_user, [(recipe),(username)])
            if c.fetchall():
                return True
            else:
                insert = 'INSERT INTO favoriterecipes(username,recipe,link) VALUES(?,?,?)'
                c.execute(insert, [(username), (recipe), (link)])
                db.commit()
                return True

    def remove_favorite_recipe(self,username,recipe):
        with sqlite3.connect('RecipeRecommender.db') as db:
            print("connected")
            c = db.cursor()
            find_user = ('DELETE FROM favoriterecipes WHERE username = ? AND recipe = ?')
            res = c.execute(find_user, [(username),(recipe)])
            if res:
                return True
            else:
                return False

    def get_favorite_recipe(self,username):
        with sqlite3.connect('RecipeRecommender.db') as db:
            c = db.cursor()
            find_user = ('SELECT recipe,link FROM favoriterecipes WHERE username = ?')
            c.execute(find_user, (username,))
            rows = c.fetchall()
            if rows:
                return rows