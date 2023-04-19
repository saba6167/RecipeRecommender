from tkinter import *
from tkinter import messagebox as ms
from tkinter import ttk
from controller import RecipeController
from controller import ViewController

class UserProfileView:
    def __init__(self, root):
        self.root = root

        #### UserProfileFrame ####
        self.user_profile_frame = None
        self.ingredients_entry = None
        self.ingredients_entry_line = None
        self.get_recipe_button = None
        self.recipe_table_frame = None
        self.recipe_table = None
        self.recipe_controller = RecipeController()
        self.view_controller = ViewController()
        self.favorite_dict = {}

        self.user_profile_frame = Frame(self.root, width=925, height=500, bg='white')
        self.ingredients_entry = Entry(self.user_profile_frame, width=25, fg='black', border=0, bg='white',
                                       font=('Microsoft YaHei UI Light', 11))
        self.ingredients_entry.place(relx=0.12, rely=0.15)
        self.ingredients_entry.insert(0, 'Ingredients')
        self.ingredients_entry.bind('<FocusIn>', self.on_enter_ingredients_entry)
        self.ingredients_entry.bind('<FocusOut>', self.on_leave_ingredients_entry)
        self.ingredients_entry_line = Frame(self.user_profile_frame, width=295, height=2, bg='black')
        self.ingredients_entry_line.place(relx=0.1, rely=0.20)
        self.get_recipe_button = Button(self.user_profile_frame, width=14, text='Get Recipe', border=0, cursor='hand2',
                                        bg='#57a1f8',fg='white')
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
        self.recipe_table = ttk.Treeview(self.recipe_table_frame, columns=("recipe", "link","favorite"), show="headings")
        self.recipe_table.heading("recipe", text="Recipe")
        self.recipe_table.heading("link", text="Link")
        self.recipe_table.heading("favorite", text="Favorite")

        self.recipe_table.bind("<Button-1>", self.highlight_row)

        self.recipe_table.pack(fill="both", expand=True)

        # Resize the columns automatically based on the cell contents
        self.recipe_table.column("recipe", width=150, stretch=True)
        self.recipe_table.column("link", width=250, stretch=True)
        self.recipe_table.column("favorite", width=75, stretch=True,anchor="center")

    def on_enter_ingredients_entry(self, e):
        self.ingredients_entry.delete(0, 'end')

    def on_leave_ingredients_entry(self, e):
        if self.ingredients_entry.get() == '':
            self.ingredients_entry.insert(0, 'Ingredients')

    def highlight_row(self, event):
        rowid = self.recipe_table.identify_row(event.y)
        self.recipe_table.selection_set(rowid)