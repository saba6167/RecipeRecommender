from tkinter import *
from controller import ViewController

class SigninView:
    def __init__(self,root):

        self.root = root

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

        self.signin_frame = Frame(self.root, width=925, height=500, bg='white')
        self.signin_frame.place(x=0, y=0)
        self.login_image = PhotoImage(file='login.png')
        self.image_label = Label(self.signin_frame, image=self.login_image, bg='white')
        self.image_label.place(x=50, y=50)
        self.signin_heading_label = Label(self.signin_frame, text='Sign in', fg='#57a1f8', bg='white',
                                          font=('Microsoft YaHei UI Light', 23, 'bold'))
        self.signin_heading_label.place(x=580, y=75)
        self.signin_user_entry = Entry(self.signin_frame, width=25, fg='black', border=0, bg='white',
                                       font=('Microsoft YaHei UI Light', 11))
        self.signin_user_entry.place(x=510, y=150)
        self.signin_user_entry.insert(0, 'Username')
        self.signin_user_line = Frame(self.signin_frame, width=295, height=2, bg='black')
        self.signin_user_line.place(x=505, y=177)
        self.signin_user_entry.bind('<Enter>', self.on_enter_signin_user_entry)
        self.signin_user_entry.bind('<Leave>', self.on_leave_signin_user_entry)
        self.signin_pwd_entry = Entry(self.signin_frame, width=25, fg='black', border=0, bg='white',
                                      font=('Microsoft YaHei UI Light', 11))
        self.signin_pwd_entry.place(x=510, y=220)
        self.signin_pwd_entry.insert(0, 'Password')
        # self.signin_pwd_entry.configure(show="*")
        self.signin_pwd_entry.bind('<Enter>', self.on_enter_signin_password_entry)
        self.signin_pwd_entry.bind('<Leave>', self.on_leave_signin_password_entry)
        self.signin_pwd_line = Frame(self.signin_frame, width=295, height=2, bg='black')
        self.signin_pwd_line.place(x=505, y=247)
        self.signin_button = Button(self.signin_frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white',
                                    border=0)
        self.signin_button.place(x=515, y=274)

        self.signin_dont_have_account_label = Label(self.signin_frame, text="Dont have an account?", fg='black',
                                                    bg='white',
                                                    font=('Microsoft YaHei UI Light', 9))
        self.signin_dont_have_account_label.place(x=555, y=340)

        self.signin_frame_signup_button  = Button(self.signin_frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8')
        self.signin_frame_signup_button .place(x=695, y=340)

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
