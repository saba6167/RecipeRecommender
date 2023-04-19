from tkinter import *
from tkinter import messagebox as ms
from tkinter import ttk
from controller import ViewController
from controller import RecipeController

class View:
    def __init__(self, root):
        self.root = root
        # self.root = Tk()
        self.root.title('Recipe Recommender System')
        self.root.geometry('925x500+300+200')
        self.root.configure(bg="#fff")
        self.root.resizable(False, False)

        ##### SigninFrame ####
        self.success_user_name = ''
        self.signin_frame = None
        self.login_image = None
        self.image_label = None
        self.signin_heading_label = None
        self.signin_user_entry = None
        self.signin_user_line = None
        self.signin_pwd_entry = None
        self.signin_pwd_line = None
        self.signin_button = None
        self.signin_dont_have_account_label = None
        self.signin_frame_signup_button = None
        self.view_controller = ViewController()

        #### SignupFrame ####
        self.signup_frame = None
        self.signup_image = None
        self.signup_image_label = None
        self.signup_heading_label = None
        self.signup_user_entry = None
        self.signup_user_line = None
        self.signup_pwd_entry = None
        self.signup_pwd_line = None
        self.signup_confirm_pwd_entry = None
        self.signup_confirm_pwd_entry_line = None
        self.signup_button = None
        self.signup_have_account_label = None
        self.signup_frame_signin_button = None

        #### UserProfileFrame ####
        self.user_profile_frame = None
        self.ingredients_entry = None
        self.ingredients_entry_line = None
        self.get_recipe_button = None
        self.recipe_table_frame = None
        self.recipe_table = None
        self.recipe_controller=RecipeController()

        ### Views
        self.create_signin_view()
        self.create_signup_view()
        self.create_user_profile_view()

    def on_enter_signin_user_entry(self, e):
        self.signin_user_entry.delete(0, 'end')

    def on_leave_signin_user_entry(self, e):
        name = self.signin_user_entry.get()
        if name == '':
            self.signin_user_entry.insert(0, 'Username')

    def on_enter_signin_password_entry(self, e):
        self.signin_pwd_entry.delete(0, 'end')

    def on_leave_signin_password_entry(self, e):
        name = self.signin_pwd_entry.get()
        if name == '':
            self.signin_pwd_entry.insert(0, 'Password')

    def clear_signin_fields(self):
        self.signin_user_entry.delete(0, END)
        self.signin_pwd_entry.delete(0, END)
        self.signin_user_entry.insert(0, 'Username')
        self.signin_pwd_entry.insert(0, 'Password')

    def logout(self):
        self.user_profile_frame.place_forget()
        self.signin_frame.place(x=0, y=0)

    def show_logout_menu(self,event):
        # Create a menu to display logout option
        menu = Menu(self.user_profile_frame, tearoff=0)
        menu.add_command(label="Logout", command=self.logout)
        menu.post(event.x_root, event.y_root)
    def signin(self):
        username = self.signin_user_entry.get()
        pwd = self.signin_pwd_entry.get()
        result = self.view_controller.check_if_user_exist(username,pwd)
        if result:
            self.success_user_name = username
            self.clear_signin_fields()
            avatar_frame = Frame(self.user_profile_frame, width=100, height=100, bg="gray")
            avatar_frame.place(width=40, height=40, relx=0.95, rely=0.02)
            name_initials = self.success_user_name[0].upper()
            initials_label = Label(avatar_frame, text=name_initials, font=("Arial", 30), fg="white", bg="gray")
            initials_label.place(relx=0.5, rely=0.5, anchor=CENTER)
            initials_label.bind("<Button-1>", self.show_logout_menu)
            Label(self.user_profile_frame, text="User Profile", bg='white', font=("Arial", 16)).place(relx=0.5, rely=0.05,
                                                                                                anchor=CENTER)
            Label(self.user_profile_frame, bg='white', text=f"Name: {self.success_user_name}").place(relx=0.5, rely=0.1,
                                                                                          anchor=CENTER)
            self.signin_frame.place_forget()
            self.user_profile_frame.place(x=0, y=0)
        else:
            self.clear_signin_fields()
            ms.showerror('Oops!', 'Username Not Found.')

    def create_account_frame(self):
        self.signin_frame.place_forget()
        self.signup_frame.place(x=0, y=0)
    def create_signin_view(self):
        self.signin_frame = Frame(self.root,width=925,height=500,bg='white')
        self.signin_frame.place(x=0,y=0)
        self.login_image = PhotoImage(file='login.png')
        self.image_label = Label(self.signin_frame, image=self.login_image, bg='white')
        self.image_label.place(x=50, y=50)
        self.signin_heading_label = Label(self.signin_frame, text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
        self.signin_heading_label.place(x=580, y=75)
        self.signin_user_entry = Entry(self.signin_frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        self.signin_user_entry.place(x=510, y=150)
        self.signin_user_entry.insert(0, 'Username')
        self.signin_user_line = Frame(self.signin_frame, width=295, height=2, bg='black')
        self.signin_user_line.place(x=505, y=177)
        self.signin_user_entry.bind('<Enter>', self.on_enter_signin_user_entry)
        self.signin_user_entry.bind('<Leave>', self.on_leave_signin_user_entry)
        self.signin_pwd_entry = Entry(self.signin_frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        self.signin_pwd_entry.place(x=510, y=220)
        self.signin_pwd_entry.insert(0, 'Password')
        # self.signin_pwd_entry.configure(show="*")
        self.signin_pwd_entry.bind('<Enter>', self.on_enter_signin_password_entry)
        self.signin_pwd_entry.bind('<Leave>', self.on_leave_signin_password_entry)
        self.signin_pwd_line = Frame(self.signin_frame, width=295, height=2, bg='black')
        self.signin_pwd_line.place(x=505, y=247)
        self.signin_button = Button(self.signin_frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, command=self.signin)
        self.signin_button.place(x=515, y=274)

        self.signin_dont_have_account_label = Label(self.signin_frame, text="Dont have an account?", fg='black', bg='white',
                      font=('Microsoft YaHei UI Light', 9))
        self.signin_dont_have_account_label.place(x=555, y=340)

        sign_up = Button(self.signin_frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8',
                         command=self.create_account_frame)
        sign_up.place(x=695, y=340)

    def on_enter_signup_user_entry(self, e):
        self.signup_user_entry.delete(0, END)

    def on_leave_signup_user_entry(self, e):
        if self.signup_user_entry.get() == '':
            self.signup_user_entry.insert(0, 'Username')

    def on_enter_signup_password_entry(self, e):
        self.signup_pwd_entry.delete(0, 'end')

    def on_leave_signup_password_entry(self, e):
        if self.signup_pwd_entry.get() == '':
            self.signup_pwd_entry.insert(0, 'Password')

    def on_enter_signup_conf_pwd_entry(self, e):
        self.signup_confirm_pwd_entry.delete(0, END)

    def on_leave_signup_conf_pwd_entry(self, e):
        if self.signup_confirm_pwd_entry.get() == '':
            self.signup_confirm_pwd_entry.insert(0, 'Confirm Password')

    def clear_signup_fields(self):
        self.signup_user_entry.delete(0, END)
        self.signup_pwd_entry.delete(0, END)
        self.signup_confirm_pwd_entry.delete(0, END)
        self.signup_user_entry.insert(0, 'Username')
        self.signup_pwd_entry.insert(0, 'Password')
        self.signup_confirm_pwd_entry.insert(0, 'Confirm Password')

    def log(self):
        self.signup_user_entry.delete(0, END)
        self.signup_pwd_entry.delete(0, END)
        self.signup_confirm_pwd_entry.delete(0, END)
        self.signup_user_entry.insert(0, 'end')
        self.signup_pwd_entry.insert(0, 'end')
        self.signup_confirm_pwd_entry.insert(0, 'end')
        self.signup_frame.place_forget()
        self.signin_frame.place(x=0, y=0)

    def new_user(self):
        p1 = self.signup_pwd_entry.get()
        p2 = self.signup_confirm_pwd_entry.get()
        if self.signup_user_entry.get() != '' and p1 != '' and p2 != '':
            if p1 == p2:
                result = self.view_controller.add_user_to_database(self.signup_user_entry.get(), p1)
                if result:
                    ms.showerror('Error!', 'Username Taken Try a Diffrent One.')
                    self.clear_signup_fields()
                else:
                    ms.showinfo('Success!', 'Account Created!')
                    self.log()
            else:
                ms.showerror('Error!', 'Both Password Should Match')
                self.clear_signup_fields()
        else:
            ms.showerror('Error!', 'All Fields Required')

    def show_signin_frame(self):
        self.signup_frame.place_forget()
        self.signin_frame.place(x=0, y=0)

    def create_signup_view(self):
        self.signup_frame = Frame(self.root,width=925,height=500,bg='#fff')
        self.signup_image = PhotoImage(file='signup.png')
        Label(self.signup_frame, image=self.signup_image, border=0, bg='white').place(x=50, y=90)
        self.signup_heading_label = Label(self.signup_frame, text='Sign up', fg='#57a1f8', bg='white',
                        font=('Microsoft Yahei UI Light', 23, 'bold'))
        self.signup_heading_label.place(x=580, y=75)
        self.signup_user_entry = Entry(self.signup_frame, width=25, fg='black', border=0, bg='white',
                            font=('Microsoft Yahei UI Light', 11))
        self.signup_user_entry.place(x=510, y=150)
        self.signup_user_entry.insert(0, 'Username')
        self.signup_user_entry.bind('<Enter>', self.on_enter_signup_user_entry)
        self.signup_user_entry.bind('<Leave>', self.on_leave_signup_user_entry)
        self.signup_user_line = Frame(self.signup_frame, width=295, height=2, bg='black')
        self.signup_user_line.place(x=505, y=177)

        self.signup_pwd_entry = Entry(self.signup_frame, width=25, fg='black', border=0, bg='white',
                                font=('Microsoft Yahei UI Light', 11))
        self.signup_pwd_entry.place(x=510, y=220)
        self.signup_pwd_entry.insert(0, 'Password')
        self.signup_pwd_entry.bind('<Enter>', self.on_enter_signup_password_entry)
        self.signup_pwd_entry.bind('<Leave>', self.on_leave_signup_password_entry)
        self.signup_pwd_line = Frame(self.signup_frame,width=295,height=2,bg='black')
        self.signup_pwd_line.place(x=505,y=247)
        
        self.signup_confirm_pwd_entry = Entry(self.signup_frame, width=25, fg='black', border=0, bg='white',
                                   font=('Microsoft Yahei UI Light', 11))
        self.signup_confirm_pwd_entry.place(x=510, y=290)
        self.signup_confirm_pwd_entry.insert(0, 'Confirm Password')
        self.signup_confirm_pwd_entry.bind('<Enter>', self.on_enter_signup_conf_pwd_entry)
        self.signup_confirm_pwd_entry.bind('<Leave>', self.on_leave_signup_conf_pwd_entry)

        self.signup_confirm_pwd_entry_line = Frame(self.signup_frame, width=295, height=2, bg='black')
        self.signup_confirm_pwd_entry_line.place(x=505, y=317)

        self.signup_button = Button(self.signup_frame, width=39, pady=7, text='Sign up', bg='#57a1f8', fg='white', border=0,
               command=self.new_user)
        self.signup_button.place(x=515, y=350)
        self.signup_have_account_label = Label(self.signup_frame, text='I have an account', fg='black', bg='white',
                      font=('Microsoft YaHei UI Light', 9))
        self.signup_have_account_label.place(x=570, y=410)

        self.signup_frame_signin_button = Button(self.signup_frame, width=6, text='Sign in', border=0, bg='white', cursor='hand2', fg='#57a1f8',
                              command=self.show_signin_frame)
        self.signup_frame_signin_button.place(x=680, y=410)

    def on_enter_ingredients_entry(self,e):
        self.ingredients_entry.delete(0, 'end')

    def on_leave_ingredients_entry(self,e):
        if self.ingredients_entry.get() == '':
            self.ingredients_entry.insert(0, 'Ingredients')

    def get_recipes(self):
        input_str = self.ingredients_entry.get()
        rec = self.recipe_controller.get_recommendations(input_str)
        recipe = rec['recipe'].tolist()
        links = rec['url'].tolist()
        for i in range(len(rec)):
            self.recipe_table.insert("", "end", values=(recipe[i], links[i]))

    def highlight_row(self,event):
        rowid = self.recipe_table.identify_row(event.y)
        self.recipe_table.selection_set(rowid)

    def create_user_profile_view(self):
        self.user_profile_frame = Frame(self.root, width=925, height=500, bg='white')
        self.ingredients_entry = Entry(self.user_profile_frame, width=25, fg='black', border=0, bg='white',
                            font=('Microsoft YaHei UI Light', 11))
        self.ingredients_entry.place(relx=0.12, rely=0.15)
        self.ingredients_entry.insert(0, 'Ingredients')
        self.ingredients_entry.bind('<FocusIn>', self.on_enter_ingredients_entry)
        self.ingredients_entry.bind('<FocusOut>', self.on_leave_ingredients_entry)
        self.ingredients_entry_line = Frame(self.user_profile_frame, width=295, height=2, bg='black')
        self.ingredients_entry_line.place(relx=0.1, rely=0.20)
        self.get_recipe_button = Button(self.user_profile_frame, width=14, text='Get Recipe', border=0, cursor='hand2', bg='#57a1f8',
                                fg='white', command=self.get_recipes)
        self.get_recipe_button.place(relx=0.45, rely=0.18)

        ##### Table frame##########
        self.recipe_table_frame = Frame(self.user_profile_frame, width=925, height=500, bg='red')
        self.recipe_table_frame.place(relwidth=0.8, relheight=0.67, relx=0.1, rely=0.3)

        # Create a style for the Treeview widget
        style = ttk.Style()
        style.theme_use("default")  # Choose your preferred theme, e.g. "vista"

        # Change the font of the Treeview headers and cell contents
        style.configure("Treeview.Heading", font=("Arial", 12))
        style.configure("Treeview", font=("Arial", 10))

        # Change the background color of the Treeview headers and cell contents
        style.map("Treeview", background=[("selected", "#99c2ff")])

        # Change the color of the Treeview border lines
        style.map("Treeview", foreground=[("focus", "black")], background=[("focus", "#FF0000")])

        # Add column separator lines
        style.configure("Treeview.Separator", background="#CACACA")

        # Create the Treeview widget
        self.recipe_table = ttk.Treeview(self.recipe_table_frame, columns=("recipe", "link"), show="headings")
        self.recipe_table.heading("recipe", text="Recipe")
        self.recipe_table.heading("link", text="Link")

        self.recipe_table.bind("<Button-1>", self.highlight_row)

        self.recipe_table.pack(fill="both", expand=True)

        # Resize the columns automatically based on the cell contents
        self.recipe_table.column("recipe", width=150, stretch=True)
        self.recipe_table.column("link", width=250, stretch=True)
