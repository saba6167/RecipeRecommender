from tkinter import *
from tkinter import messagebox as ms
from MVC.Views.SignInView import SigninView
from MVC.Views.SignUpView import SignupView
from MVC.Views.UserProfileView import UserProfileView
import webbrowser
from Observer.RecipeObserver import RecipeObserver
from Observer.RecipeHistory import RecipeHistory

class RecipeRecommenderSystem:
    __instance = None

    def __init__(self):
        # Creating a singleton instance
        if RecipeRecommenderSystem.__instance is not None:
            raise Exception("Singleton instance already exists")
        else:
            # Creating a root window and configuring its properties
            self.root = Tk()
            self.root.title('RRS')
            self.root.geometry('925x500+300+200')
            self.root.configure(bg="#fff")
            self.root.resizable(False, False)

            # Creating instances of RecipeObserver and RecipeHistory classes
            self.recipe_observer = RecipeObserver()
            self.history = RecipeHistory()

            # Attaching RecipeHistory object to RecipeObserver object
            self.recipe_observer.attach(self.history)

            # Creating an instance of SigninView class and configuring its buttons
            self.signin_screen = SigninView(self.root)
            self.signin_screen.signin_frame_signup_button.configure(command=self.create_account_frame)
            self.signin_screen.signin_frame_signup_button.update()
            self.signin_screen.signin_button.configure(command=self.signin)
            self.signin_screen.signin_button.update()

            # Creating an instance of SignupView class and configuring its buttons
            self.signup_screen = SignupView(self.root)
            self.signup_screen.signup_button.configure(command=self.new_user)
            self.signup_screen.signup_button.update()
            self.signup_screen.signup_frame_signin_button.configure(command=self.show_signin_frame)
            self.signup_screen.signup_frame_signin_button.update()

            # Creating an instance of UserProfileView class and configuring its buttons and table
            self.userProfile_screen = UserProfileView(self.root)
            self.userProfile_screen.get_recipe_button.configure(command=self.get_recipes)
            self.userProfile_screen.get_recipe_button.update()
            self.userProfile_screen.recipe_table.bind("<Double-Button-1>", self.open_link)
            self.userProfile_screen.recipe_table.bind("<Button-1>", self.handle_click)

            # Creating the singleton instance of Application class
            self.__class__.__instance = self

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls()
        return cls.__instance

    # This method is called when the "create account" button is clicked in the signin frame
    # It hides the signin frame and displays the signup frame
    def create_account_frame(self):
        self.signin_screen.signin_frame.place_forget()
        self.signup_screen.signup_frame.place(x=0, y=0)

    # This method logs out the user by hiding the user profile frame and displaying the signin frame
    # It also clears the recipe table and ingredients entry
    def logout(self):
        self.userProfile_screen.user_profile_frame.place_forget()
        self.signin_screen.signin_frame.place(x=0, y=0)
        self.userProfile_screen.recipe_table.delete(*self.userProfile_screen.recipe_table.get_children())
        self.userProfile_screen.ingredients_entry.delete(0, 'end')

    # This method shows the user's history in the recipe table
    def show_history(self):
        # Delete previous values from the table
        self.userProfile_screen.recipe_table.delete(*self.userProfile_screen.recipe_table.get_children())
        # Insert new values into the table
        result = self.userProfile_screen.view_controller.get_history_from_database(self.signin_screen.success_user_name)
        if result:
            favorite_recipes = self.userProfile_screen.view_controller.get_favorite_recipes_from_database(
                self.signin_screen.success_user_name)
            for value in result:
                value = list(value)
                if favorite_recipes:
                    if value[0] in [favorite_recipe[0] for favorite_recipe in favorite_recipes]:
                        self.userProfile_screen.recipe_table.insert("", "end", values=(value[0], value[1], "Yes"))
                        self.userProfile_screen.favorite_dict[value[0]] = True
                    else:
                        self.userProfile_screen.recipe_table.insert("", "end", values=(value[0], value[1], "No"))
                        self.userProfile_screen.favorite_dict[value[0]] = False
                else:
                    self.userProfile_screen.recipe_table.insert("", "end", values=(value[0], value[1], "No"))
                    self.userProfile_screen.favorite_dict[value[0]] = False
        else:
            # Display an error message if the user has no history yet
            ms.showerror("Note", "You dont have any history yet")

    def show_favorite_recipes(self):
        # Delete previous values from the table
        self.userProfile_screen.recipe_table.delete(*self.userProfile_screen.recipe_table.get_children())
        # Insert new values into the table
        result = self.userProfile_screen.view_controller.get_favorite_recipes_from_database(
            self.signin_screen.success_user_name)
        if result:
            for value in result:
                value = list(value)
                value.append("Yes")
                self.userProfile_screen.favorite_dict[value[0]] = True
                self.userProfile_screen.recipe_table.insert("", "end", values=value)
        else:
            ms.showerror("Note", "You dont have favorite recipes yet")

    def show_logout_menu(self, event):
        # Create a menu to display logout option
        menu = Menu(self.userProfile_screen.user_profile_frame, tearoff=0)
        menu.add_command(label="Logout", command=self.logout)
        menu.add_command(label="History", command=self.show_history)
        menu.add_command(label="Favorite Recipes", command=self.show_favorite_recipes)
        menu.post(event.x_root, event.y_root)

    def signin(self):
        username = self.signin_screen.signin_user_entry.get()
        pwd = self.signin_screen.signin_pwd_entry.get()
        print(username, pwd)
        user_exist, pass_correct = self.signin_screen.view_controller.check_if_user_exist(username, pwd)
        if username != "Username" and pwd != "Password":
            if len(pass_correct) == 1:
                # If username and password are correct
                self.signin_screen.success_user_name = username
                self.clear_signin_fields()
                # Create an avatar frame and display user's name initials
                avatar_frame = Frame(self.userProfile_screen.user_profile_frame, width=100, height=100, bg="gray")
                avatar_frame.place(width=40, height=40, relx=0.95, rely=0.02)
                name_initials = self.signin_screen.success_user_name[0].upper()
                initials_label = Label(avatar_frame, text=name_initials, font=("Arial", 30), fg="white", bg="gray")
                initials_label.place(relx=0.5, rely=0.5, anchor=CENTER)
                initials_label.bind("<Button-1>", self.show_logout_menu)
                # Display user's profile information
                Label(self.userProfile_screen.user_profile_frame, text="User Profile", bg='white',
                      font=("Arial", 16)).place(
                    relx=0.5, rely=0.05, anchor=CENTER)
                Label(self.userProfile_screen.user_profile_frame, bg='white',
                      text=f"Name: {self.signin_screen.success_user_name}").place(relx=0.5, rely=0.1,
                                                                                  anchor=CENTER)
                # Switch from the signin frame to the user profile frame
                self.signin_screen.signin_frame.place_forget()
                self.userProfile_screen.user_profile_frame.place(x=0, y=0)
            elif len(user_exist) == 1 and len(pass_correct) == 0:
                # If password is incorrect
                self.clear_signin_fields()
                ms.showerror('Oops!', 'Password is incorrect.')
            else:
                # If username does not exist
                ms.showerror('Oops!', 'Username does not exist.')
        else:
            ms.showerror("Error", "All fields required")

    # Function to clear the signin entry fields
    def clear_signin_fields(self):
        # Clear the fields
        self.signin_screen.signin_user_entry.delete(0, END)
        self.signin_screen.signin_pwd_entry.delete(0, END)
        # Insert default values
        self.signin_screen.signin_user_entry.insert(0, 'Username')
        self.signin_screen.signin_pwd_entry.insert(0, 'Password')

    # Function to clear the signup entry fields
    def clear_signup_fields(self):
        # Clear the fields
        self.signup_screen.signup_user_entry.delete(0, END)
        self.signup_screen.signup_pwd_entry.delete(0, END)
        self.signup_screen.signup_confirm_pwd_entry.delete(0, END)
        # Insert default values
        self.signup_screen.signup_user_entry.insert(0, 'Username')
        self.signup_screen.signup_pwd_entry.insert(0, 'Password')
        self.signup_screen.signup_confirm_pwd_entry.insert(0, 'Confirm Password')

    # Function to log out the user
    def log(self):
        # Clear the signup entry fields
        self.signup_screen.signup_user_entry.delete(0, END)
        self.signup_screen.signup_pwd_entry.delete(0, END)
        self.signup_screen.signup_confirm_pwd_entry.delete(0, END)
        # Insert values to fill the fields
        self.signup_screen.signup_user_entry.insert(0, 'end')
        self.signup_screen.signup_pwd_entry.insert(0, 'end')
        self.signup_screen.signup_confirm_pwd_entry.insert(0, 'end')
        # Hide the signup frame and show the signin frame
        self.signup_screen.signup_frame.place_forget()
        self.signin_screen.signin_frame.place(x=0, y=0)

    def new_user(self):
        # Get user input for password and confirmation password
        p1 = self.signup_screen.signup_pwd_entry.get()
        p2 = self.signup_screen.signup_confirm_pwd_entry.get()
        print(p1, p2)
        # Check if all fields are filled out
        if self.signup_screen.signup_user_entry.get() != 'Username' and p1 != 'Password' and p2 != 'Confirm Password':
            # Check if passwords match
            if p1 == p2:
                # Add new user to database
                result = self.signup_screen.view_controller.add_user_to_database(
                    self.signup_screen.signup_user_entry.get(), p1)
                if result:
                    # Username already taken, display error message and clear fields
                    ms.showerror('Error!', 'Username Taken Try a Different One.')
                    self.clear_signup_fields()
                else:
                    # Account created successfully, display success message and switch to login screen
                    ms.showinfo('Success!', 'Account Created!')
                    self.log()
            else:
                # Passwords don't match, display error message and clear fields
                ms.showerror('Error!', 'Both Password Should Match')
                self.clear_signup_fields()
        else:
            # Not all fields are filled out, display error message
            ms.showerror('Error!', 'All Fields Required')

    def show_signin_frame(self):
        # Switch to login screen
        self.signup_screen.signup_frame.place_forget()
        self.signin_screen.signin_frame.place(x=0, y=0)

    def open_link(self,event):
        # Get recipe and link for selected item in table
        item = self.userProfile_screen.recipe_table.selection()[0]
        values = self.userProfile_screen.recipe_table.item(item, "values")
        recipe, link = values[0], values[1]
        # Notify observers of recipe selection and open link in new tab
        res = self.recipe_observer.notify(self.userProfile_screen.view_controller, self.signin_screen.success_user_name,
                                          recipe, link)
        print(res)
        if res:
            print("inserted")
        webbrowser.open_new_tab(link)

    def get_recipe_index(self, recipe):
        # Return the index of the row containing the recipe
        for child in self.userProfile_screen.recipe_table.get_children():
            if self.userProfile_screen.recipe_table.item(child)["values"][0] == recipe:
                return child

    def update_checkbox(self, recipe):
        # Update the checkbox in the table
        if self.userProfile_screen.favorite_dict[recipe]:
            value = "Yes"
        else:
            value = "No"
        index = self.get_recipe_index(recipe)
        self.userProfile_screen.recipe_table.set(index, "#3", value)

    def toggle_favorite(self, recipe, link):
        # Toggle the favorite status of a recipe
        self.userProfile_screen.favorite_dict[recipe] = not self.userProfile_screen.favorite_dict[recipe]
        self.update_checkbox(recipe)

        if self.userProfile_screen.favorite_dict[recipe]:
            result = self.userProfile_screen.view_controller.add_favorite_recipe_to_database(
                self.signin_screen.success_user_name, recipe, link)
            if result:
                ms.showinfo("Success", "Added to favorite")

        else:
            result = self.userProfile_screen.view_controller.remove_favorite_recipe_from_database(
                self.signin_screen.success_user_name, recipe)
            if result:
                ms.showinfo("Success", "Removed from favorite")
            else:
                ms.showinfo("Failed", "Unable to delete")

    def handle_click(self, event):
        # Handle clicks on the favorite checkbox
        if self.userProfile_screen.recipe_table.identify_region(event.x, event.y) == "cell":
            col = self.userProfile_screen.recipe_table.identify_column(event.x)
            if col == "#3":
                index = self.userProfile_screen.recipe_table.identify_row(event.y)
                recipe = self.userProfile_screen.recipe_table.item(index)["values"][0]
                link = self.userProfile_screen.recipe_table.item(index)["values"][1]
                self.toggle_favorite(recipe, link)

    def get_recipes(self):
        # Get the user input from the ingredients entry box
        input_str = self.userProfile_screen.ingredients_entry.get()
        # Clear the existing recipes in the table
        self.userProfile_screen.recipe_table.delete(*self.userProfile_screen.recipe_table.get_children())
        # Get recipe recommendations based on the user input
        rec = self.userProfile_screen.recipe_controller.get_recommendations(input_str)
        # print(rec['ingredients'].tolist()[0])
        print(rec)
        # If at least one recipe is found:
        if len(rec) >= 1:
            # Get the names and links of the recommended recipes
            recipe = rec['recipe'].tolist()
            links = rec['url'].tolist()
            # Get the list of user's favorite recipes from the database
            favorite_recipes = self.userProfile_screen.view_controller.get_favorite_recipes_from_database(
                self.signin_screen.success_user_name)
            # Add the recipes to the table and mark the favorite ones with a checkbox
            for i in range(len(rec)):
                # If the user has favorite recipes:
                if favorite_recipes:
                    # Check if the current recipe is in the user's favorite recipes list
                    if recipe[i] in [favorite_recipe[0] for favorite_recipe in favorite_recipes]:
                        # Mark the recipe as favorite and add it to the table
                        self.userProfile_screen.recipe_table.insert("", "end", values=(recipe[i], links[i], "Yes"))
                        self.userProfile_screen.favorite_dict[recipe[i]] = True
                    else:
                        # Add the recipe to the table but don't mark it as favorite
                        self.userProfile_screen.recipe_table.insert("", "end", values=(recipe[i], links[i], "No"))
                        self.userProfile_screen.favorite_dict[recipe[i]] = False
                else:
                    # Add the recipe to the table and don't mark it as favorite (since the user has no favorite recipes)
                    self.userProfile_screen.recipe_table.insert("", "end", values=(recipe[i], links[i], "No"))
                    self.userProfile_screen.favorite_dict[recipe[i]] = False
        else:
            # Show an error message if no recipes are found with the given ingredients
            ms.showerror("Error", "No recipe exist with such ingredients")