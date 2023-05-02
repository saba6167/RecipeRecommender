from tkinter import *
from MVC.Controllers.ViewsController import ViewController
from PIL import Image, ImageTk, ImageSequence

class SignupView:
    def __init__(self, root):
        self.root = root

        # Signup Frame Widgets
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
        self.view_controller = ViewController()
        self.frames = None

        # Creating the Signup frame
        self.signup_frame = Frame(self.root, width=925, height=500, bg='#fff')

        # Load and display the signup gif
        self.frames = self.load_frames(r'C:\Users\mehmo\AppData\Roaming\JetBrains\PyCharmCE2022.2\scratches\RecipeRecommendationSystem_V1\MVC\Views\signup.gif')
        label = Label(self.signup_frame, border=0, bg='white')
        label.place(x=50, y=40)
        label.cancel = label.after(0, self.play, self.frames, label)

        # Signup heading label
        self.signup_heading_label = Label(self.signup_frame, text='Sign up', fg='#57a1f8', bg='white',
                                          font=('Microsoft Yahei UI Light', 23, 'bold'))
        self.signup_heading_label.place(x=580, y=75)
        # Username entry field
        self.signup_user_entry = Entry(self.signup_frame, width=25, fg='black', border=0, bg='white',
                                       font=('Microsoft Yahei UI Light', 11))
        self.signup_user_entry.place(x=510, y=150)
        self.signup_user_entry.insert(0, 'Username')

        # Binding the signup_user_entry
        self.signup_user_entry.bind('<Enter>', self.on_enter_signup_user_entry)
        self.signup_user_entry.bind('<Leave>', self.on_leave_signup_user_entry)
        self.signup_user_line = Frame(self.signup_frame, width=295, height=2, bg='black')
        self.signup_user_line.place(x=505, y=177)

        # Password entry field
        self.signup_pwd_entry = Entry(self.signup_frame, width=25, fg='black', border=0, bg='white',
                                      font=('Microsoft Yahei UI Light', 11))
        self.signup_pwd_entry.place(x=510, y=220)
        self.signup_pwd_entry.insert(0, 'Password')

        # Binding the signup_pwd_entry on_enter and on_leave functionalities
        self.signup_pwd_entry.bind('<Enter>', self.on_enter_signup_password_entry)
        self.signup_pwd_entry.bind('<Leave>', self.on_leave_signup_password_entry)
        self.signup_pwd_line = Frame(self.signup_frame, width=295, height=2, bg='black')
        self.signup_pwd_line.place(x=505, y=247)

        # Confirm password entry field
        self.signup_confirm_pwd_entry = Entry(self.signup_frame, width=25, fg='black', border=0, bg='white',
                                              font=('Microsoft Yahei UI Light', 11))
        self.signup_confirm_pwd_entry.place(x=510, y=290)
        self.signup_confirm_pwd_entry.insert(0, 'Confirm Password')

        # Binding the signup_confirm_pwd_entry on_enter and on_leave functionalities
        self.signup_confirm_pwd_entry.bind('<Enter>', self.on_enter_signup_conf_pwd_entry)
        self.signup_confirm_pwd_entry.bind('<Leave>', self.on_leave_signup_conf_pwd_entry)

        self.signup_confirm_pwd_entry_line = Frame(self.signup_frame, width=295, height=2, bg='black')
        self.signup_confirm_pwd_entry_line.place(x=505, y=317)

        # Signup button
        self.signup_button = Button(self.signup_frame, width=39, pady=7, text='Sign up', bg='#57a1f8', fg='white',
                                    border=0)
        self.signup_button.place(x=515, y=350)

        # "I have an account" label
        self.signup_have_account_label = Label(self.signup_frame, text='I have an account', fg='black', bg='white',
                                               font=('Microsoft YaHei UI Light', 9))
        self.signup_have_account_label.place(x=570, y=410)

        # Signin button
        self.signup_frame_signin_button = Button(self.signup_frame, width=6, text='Sign in', border=0, bg='white',
                                                 cursor='hand2', fg='#57a1f8')
        self.signup_frame_signin_button.place(x=680, y=410)

    def on_enter_signup_user_entry(self, e):
        # This function is triggered when the mouse enters the signup_user_entry field.
        # It clears the field by deleting its contents.
        self.signup_user_entry.delete(0, END)

    def on_leave_signup_user_entry(self, e):
        # This function is triggered when the mouse leaves the signup_user_entry field.
        # If the field is empty, it inserts the default text 'Username' into the field.
        if self.signup_user_entry.get() == '':
            self.signup_user_entry.insert(0, 'Username')

    def on_enter_signup_password_entry(self, e):
        # This function is triggered when the mouse enters the signup_password_entry field.
        # It clears the field by deleting its contents and configures it to show '*' characters for password input.
        self.signup_pwd_entry.delete(0, 'end')
        self.signup_pwd_entry.configure(show='*')

    def on_leave_signup_password_entry(self, e):
        # This function is triggered when the mouse leaves the signup_password_entry field.
        # If the field is empty, it inserts the default text 'Password' into the field.
        if self.signup_pwd_entry.get() == '':
            # Resets the field to display plain text instead of '*'
            self.signup_pwd_entry.configure(show="")
            self.signup_pwd_entry.insert(0, 'Password')

    def on_enter_signup_conf_pwd_entry(self, e):
        # This function is triggered when the mouse enters the signup_confirm_pwd_entry field.
        # It clears the field by deleting its contents and configures it to show '*' characters for password input.
        self.signup_confirm_pwd_entry.delete(0, END)
        self.signup_confirm_pwd_entry.configure(show='*')

    def on_leave_signup_conf_pwd_entry(self, e):
        # This function is triggered when the mouse leaves the signup_confirm_pwd_entry field.
        # If the field is empty, it inserts the default text 'Confirm Password' into the field.
        if self.signup_confirm_pwd_entry.get() == '':
            # Resets the field to display plain text instead of '*'
            self.signup_confirm_pwd_entry.configure(show="")
            self.signup_confirm_pwd_entry.insert(0, 'Confirm Password')

    def load_frames(self, path):
        # This function takes a path to an image file as input.
        # It loads the frames from the image using the Image module and returns a list of ImageTk.PhotoImage objects.
        frames = []
        with Image.open(path) as img:
            for frame in ImageSequence.Iterator(img):
                frames.append(ImageTk.PhotoImage(frame))
        return frames

    def play(self, frames, label, idx=0, delay=100):
        # This function is used to play a sequence of frames in a label widget.
        # It updates the image displayed in the label to the current frame.
        # The 'idx' parameter keeps track of the current frame index, and 'delay' specifies the time between frame updates.
        label.config(image=frames[idx])
        idx = (idx + 1) % len(frames)
        label.after(delay, self.play, frames, label, idx)

    def stop(self, label):
        # This function is used to stop the animation in the label widget.
        # It cancels the scheduled 'after' event associated with the animation.
        label.after_cancel(label.cancel)