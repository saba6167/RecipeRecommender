from tkinter import *
from tkinter import messagebox as ms
from Signin_view import SigninView
from Signup_view import SignupView
from UserProfile_view import UserProfileView
import webbrowser

if __name__ == '__main__':
    def create_account_frame():
        signin_screen.signin_frame.place_forget()
        signup_screen.signup_frame.place(x=0, y=0)


    def logout():
        userProfile_screen.user_profile_frame.place_forget()
        signin_screen.signin_frame.place(x=0, y=0)
        userProfile_screen.recipe_table.delete(*userProfile_screen.recipe_table.get_children())
        userProfile_screen.ingredients_entry.delete(0, 'end')


    def show_history():
        # Delete previous values from the table
        userProfile_screen.recipe_table.delete(*userProfile_screen.recipe_table.get_children())
        # Insert new values into the table
        result = userProfile_screen.view_controller.get_history_from_database(signin_screen.success_user_name)
        if result:
            favorite_recipes = userProfile_screen.view_controller.get_favorite_recipes_from_database(
                signin_screen.success_user_name)
            for value in result:
                value = list(value)
                if favorite_recipes:
                    if value[0] in [favorite_recipe[0] for favorite_recipe in favorite_recipes]:
                        userProfile_screen.recipe_table.insert("", "end", values=(value[0], value[1], "Yes"))
                        userProfile_screen.favorite_dict[value[0]] = True
                    else:
                        userProfile_screen.recipe_table.insert("", "end", values=(value[0], value[1], "No"))
                        userProfile_screen.favorite_dict[value[0]] = False
        else:
            ms.showerror("Note", "You dont have any history yet")


    def show_favorite_recipes():
        # Delete previous values from the table
        userProfile_screen.recipe_table.delete(*userProfile_screen.recipe_table.get_children())
        # Insert new values into the table
        result = userProfile_screen.view_controller.get_favorite_recipes_from_database(signin_screen.success_user_name)
        if result:
            for value in result:
                value = list(value)
                value.append("Yes")
                userProfile_screen.favorite_dict[value[0]] = True
                userProfile_screen.recipe_table.insert("", "end", values=value)
        else:
            ms.showerror("Note", "You dont have favorite recipes yet")


    def show_logout_menu(event):
        # Create a menu to display logout option
        menu = Menu(userProfile_screen.user_profile_frame, tearoff=0)
        menu.add_command(label="Logout", command=logout)
        menu.add_command(label="History",command=show_history)
        menu.add_command(label="Favorite Recipes", command=show_favorite_recipes)
        menu.post(event.x_root, event.y_root)


    def signin():
        username = signin_screen.signin_user_entry.get()
        pwd = signin_screen.signin_pwd_entry.get()
        print(username,pwd)
        user_exist,pass_correct = signin_screen.view_controller.check_if_user_exist(username,pwd)
        if username!="Username" and pwd!="Password":
            if len(pass_correct)==1:
                signin_screen.success_user_name = username
                clear_signin_fields()
                avatar_frame = Frame(userProfile_screen.user_profile_frame, width=100, height=100, bg="gray")
                avatar_frame.place(width=40, height=40, relx=0.95, rely=0.02)
                name_initials = signin_screen.success_user_name[0].upper()
                initials_label = Label(avatar_frame, text=name_initials, font=("Arial", 30), fg="white", bg="gray")
                initials_label.place(relx=0.5, rely=0.5, anchor=CENTER)
                initials_label.bind("<Button-1>", show_logout_menu)
                Label(userProfile_screen.user_profile_frame, text="User Profile", bg='white', font=("Arial", 16)).place(relx=0.5, rely=0.05,
                                                                                                    anchor=CENTER)
                Label(userProfile_screen.user_profile_frame, bg='white', text=f"Name: {signin_screen.success_user_name}").place(relx=0.5, rely=0.1,
                                                                                              anchor=CENTER)
                signin_screen.signin_frame.place_forget()
                userProfile_screen.user_profile_frame.place(x=0, y=0)
            elif len(user_exist)==1 and len(pass_correct)==0:
                clear_signin_fields()
                ms.showerror('Oops!', 'Password is incorrect.')
            else:
                ms.showerror('Oops!', 'Username does not exist.')
        else:
            ms.showerror("Error","All fields required")


    def clear_signin_fields():
        signin_screen.signin_user_entry.delete(0, END)
        signin_screen.signin_pwd_entry.delete(0, END)
        signin_screen.signin_user_entry.insert(0, 'Username')
        signin_screen.signin_pwd_entry.insert(0, 'Password')


    def clear_signup_fields():
        signup_screen.signup_user_entry.delete(0, END)
        signup_screen.signup_pwd_entry.delete(0, END)
        signup_screen.signup_confirm_pwd_entry.delete(0, END)
        signup_screen.signup_user_entry.insert(0, 'Username')
        signup_screen.signup_pwd_entry.insert(0, 'Password')
        signup_screen.signup_confirm_pwd_entry.insert(0, 'Confirm Password')


    def log():
        signup_screen.signup_user_entry.delete(0, END)
        signup_screen.signup_pwd_entry.delete(0, END)
        signup_screen.signup_confirm_pwd_entry.delete(0, END)
        signup_screen.signup_user_entry.insert(0, 'end')
        signup_screen.signup_pwd_entry.insert(0, 'end')
        signup_screen.signup_confirm_pwd_entry.insert(0, 'end')
        signup_screen.signup_frame.place_forget()
        signin_screen.signin_frame.place(x=0, y=0)


    def new_user():
        p1 = signup_screen.signup_pwd_entry.get()
        p2 = signup_screen.signup_confirm_pwd_entry.get()
        print(p1,p2)
        if signup_screen.signup_user_entry.get() != 'Username' and p1 != 'Password' and p2 != 'Confirm Password':
            if p1 == p2:
                result = signup_screen.view_controller.add_user_to_database(signup_screen.signup_user_entry.get(), p1)
                if result:
                    ms.showerror('Error!', 'Username Taken Try a Different One.')
                    clear_signup_fields()
                else:
                    ms.showinfo('Success!', 'Account Created!')
                    log()
            else:
                ms.showerror('Error!', 'Both Password Should Match')
                clear_signup_fields()
        else:
            ms.showerror('Error!', 'All Fields Required')


    def show_signin_frame():
        signup_screen.signup_frame.place_forget()
        signin_screen.signin_frame.place(x=0, y=0)


    def open_link(event):
        item = userProfile_screen.recipe_table.selection()[0]
        values = userProfile_screen.recipe_table.item(item, "values")
        recipe, link = values[0], values[1]
        # link = self.recipe_table.item(item, "values")[1]
        res = userProfile_screen.view_controller.add_history_to_database(signin_screen.success_user_name,recipe,link)
        if res:
            print("inserted")
        webbrowser.open_new_tab(link)


    def get_recipe_index(recipe):
        # Return the index of the row containing the recipe
        for child in userProfile_screen.recipe_table.get_children():
            if userProfile_screen.recipe_table.item(child)["values"][0] == recipe:
                return child

    def update_checkbox(recipe):
        # Update the checkbox in the table
        if userProfile_screen.favorite_dict[recipe]:
            value = "Yes"
        else:
            value = "No"
        index = get_recipe_index(recipe)
        userProfile_screen.recipe_table.set(index, "#3", value)


    def toggle_favorite(recipe,link):
        # Toggle the favorite status of a recipe
        userProfile_screen.favorite_dict[recipe] = not userProfile_screen.favorite_dict[recipe]
        update_checkbox(recipe)

        if userProfile_screen.favorite_dict[recipe]:
            result = userProfile_screen.view_controller.add_favorite_recipe_to_database(signin_screen.success_user_name,recipe,link)
            if result:
                ms.showinfo("Success","Added to favorite")

        else:
            result = userProfile_screen.view_controller.remove_favorite_recipe_from_database(signin_screen.success_user_name,recipe)
            if result:
                ms.showinfo("Success","Removed from favorite")
            else:
                ms.showinfo("Failed","Unable to delete")

    def handle_click(event):
        # Handle clicks on the favorite checkbox
        if  userProfile_screen.recipe_table.identify_region(event.x, event.y) == "cell":
            col =  userProfile_screen.recipe_table.identify_column(event.x)
            if col == "#3":
                index =  userProfile_screen.recipe_table.identify_row(event.y)
                recipe =  userProfile_screen.recipe_table.item(index)["values"][0]
                link = userProfile_screen.recipe_table.item(index)["values"][1]
                toggle_favorite(recipe,link)

    def get_recipes():
        input_str = userProfile_screen.ingredients_entry.get()
        userProfile_screen.recipe_table.delete(*userProfile_screen.recipe_table.get_children())
        rec = userProfile_screen.recipe_controller.get_recommendations(input_str)
        # print(rec['ingredients'].tolist()[0])
        print(rec)
        if len(rec)>=1:
            recipe = rec['recipe'].tolist()
            links = rec['url'].tolist()
            favorite_recipes = userProfile_screen.view_controller.get_favorite_recipes_from_database(
                signin_screen.success_user_name)
            for i in range(len(rec)):
                if favorite_recipes:
                    if recipe[i] in [favorite_recipe[0] for favorite_recipe in favorite_recipes]:
                        userProfile_screen.recipe_table.insert("", "end", values=(recipe[i], links[i], "Yes"))
                        userProfile_screen.favorite_dict[recipe[i]] = True
                    else:
                        userProfile_screen.recipe_table.insert("", "end", values=(recipe[i], links[i], "No"))
                        userProfile_screen.favorite_dict[recipe[i]] = False
                else:
                    userProfile_screen.recipe_table.insert("", "end", values=(recipe[i], links[i],"No"))
                    userProfile_screen.favorite_dict[recipe[i]] = False
        else:
            ms.showerror("Error", "No recipe exist with such ingredients")

    root = Tk()
    root.title('Recipe Recommender')
    root.geometry('925x500+300+200')
    root.configure(bg="#fff")
    root.resizable(False, False)
    ###Signin
    signin_screen = SigninView(root)
    signin_screen.signin_frame_signup_button.configure(command=create_account_frame)
    signin_screen.signin_frame_signup_button.update()
    signin_screen.signin_button.configure(command=signin)
    signin_screen.signin_button.update()
    signup_screen = SignupView(root)

    ###Signup
    signup_screen.signup_button.configure(command=new_user)
    signup_screen.signup_button.update()
    signup_screen.signup_frame_signin_button.configure(command=show_signin_frame)
    signup_screen.signup_frame_signin_button.update()

    userProfile_screen = UserProfileView(root)
    userProfile_screen.get_recipe_button.configure(command=get_recipes)
    userProfile_screen.get_recipe_button.update()
    userProfile_screen.recipe_table.bind("<Double-Button-1>", open_link)
    userProfile_screen.recipe_table.bind("<Button-1>",handle_click)
    root.mainloop()