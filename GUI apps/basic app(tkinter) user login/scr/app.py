import tkinter as tk
from tkinter import Frame, StringVar, ttk
from tkinter.constants import CENTER
from scr.usr import User

class App(tk.Tk):
    def __init__(self, user_db: User):
        super().__init__()
        self._db = user_db
    
        self.title("Login Window")
        self.screen_size = self._get_screen_size()
        app_win_width = 400
        app_win_height = 500
        app_pos_x = round((self.screen_size[0] / 2) - app_win_width / 2)
        app_pos_y = round((self.screen_size[1] / 2) - app_win_height / 2)
        self.geometry(f"{app_win_width}x{app_win_height}+{app_pos_x}+{app_pos_y}")

        self.switch_frame(MainFrame)

    def get_db(self) -> object:
        return self._db

    def switch_frame(self, frame_class: type) -> None:
        new_frame: Frame = frame_class(self)
        self.frame = new_frame
        self.frame.place(relheight=1, relwidth=1, relx=0, rely=0)
        
    def _get_screen_size(self) -> tuple[float, float]:
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
        print(f'Monitor: {screen_width}x{screen_height}')
        return screen_width, screen_height

class MainFrame(tk.Frame):
    def __init__(self, parent: App) -> None:
        tk.Frame.__init__(self, parent)
        self._db = App.get_db(parent)
        self.parent = parent

        login_lbl = ttk.Label(self, text="LOGIN", font=('Arial', 10, 'bold'), anchor=CENTER)
        login_lbl.place(relheight=0.1, relwidth=0.8, relx=0.1, rely=0.1)

        self.login = StringVar()
        login_window = ttk.Entry(self, textvariable=self.login, justify=CENTER)
        login_window.place(relheight=0.1, relwidth=0.8, relx=0.1, rely=0.2)

        pass_lbl = ttk.Label(self, text="PASSWORD", font=('Arial', 10, 'bold'), anchor=CENTER)
        pass_lbl.place(relheight=0.1, relwidth=0.8, relx=0.1, rely=0.3)

        self.password = StringVar()
        pass_window = ttk.Entry(self, textvariable=self.password, justify=CENTER, show='*')
        pass_window.place(relheight=0.1, relwidth=0.8, relx=0.1, rely=0.4)

        self.msg_var = StringVar()
        msg_lbl = ttk.Label(self, textvariable=self.msg_var, font=('Arial, 8'), anchor=CENTER)
        msg_lbl.place(relheight=0.05, relwidth=0.8, relx=0.1, rely=0.5)

        login_btn = ttk.Button(self, text="LOG IN", command=self.log_in)
        login_btn.place(relheight=0.1, relwidth=0.6, relx=0.2, rely=0.6)

        register_lbl = ttk.Label(self, text="Don't have account yet?", font=('Arial', 8), anchor=CENTER)
        register_lbl.place(relheight=0.1, relwidth=0.8, relx=0.1, rely=0.75)
        register_btn = ttk.Button(self, text="REGISTER", command=lambda: parent.switch_frame(RegisterFrame))
        register_btn.place(relheight=0.05, relwidth=0.4, relx=0.3, rely=0.85)

    def log_in(self) -> None:
        login = self.login.get()
        password = self.password.get()
        if User.is_login_authorized(self._db, login, password):
            App.switch_frame(self.parent, SuccessfullLogIn)


class RegisterFrame(tk.Frame):
    def __init__(self, parent: App) -> None:
        tk.Frame.__init__(self, parent)
        self._db = App.get_db(parent)
        self.parent = parent

        login_btn = ttk.Button(self, text="Go back to log in.", command=lambda: parent.switch_frame(MainFrame))
        login_btn.place(relheight=0.05, relwidth=0.8, relx=0.1, rely=0.01)

        first_name_lbl = ttk.Label(self, text="Name:", anchor=CENTER)
        first_name_lbl.place(relheight=0.05, relwidth=0.8, relx=0.1, rely=0.1)

        self.new_first_name_var = StringVar()
        first_name_ent = ttk.Entry(self, textvariable=self.new_first_name_var, justify=CENTER)
        first_name_ent.place(relheight=0.05, relwidth=0.8, relx=0.1, rely=0.15)
        
        last_name_lbl = ttk.Label(self, text="Surname:", anchor=CENTER)
        last_name_lbl.place(relheight=0.05, relwidth=0.8, relx=0.1, rely=0.2)

        self.new_last_name_var = StringVar()
        last_name_ent = ttk.Entry(self, textvariable=self.new_last_name_var, justify=CENTER)
        last_name_ent.place(relheight=0.05, relwidth=0.8, relx=0.1, rely=0.25)

        new_login_lbl = ttk.Label(self, text="Login:", anchor=CENTER)
        new_login_lbl.place(relheight=0.05, relwidth=0.8, relx=0.1, rely=0.3)

        self.new_login_var = StringVar()
        new_login_ent = ttk.Entry(self, textvariable=self.new_login_var, justify=CENTER)
        new_login_ent.place(relheight=0.05, relwidth=0.8, relx=0.1, rely=0.35)

        new_pass_lbl = ttk.Label(self, text="Password:", anchor=CENTER)
        new_pass_lbl.place(relheight=0.05, relwidth=0.8, relx=0.1, rely=0.4)

        self.new_pass_var = StringVar()
        new_pass_ent = ttk.Entry(self, textvariable=self.new_pass_var, justify=CENTER)
        new_pass_ent.place(relheight=0.05, relwidth=0.8, relx=0.1, rely=0.45)

        self.error_msg = StringVar()
        error_lbl = ttk.Label(self, textvariable=self.error_msg, anchor=CENTER)
        error_lbl.place(relheight=0.05, relwidth=0.8, relx=0.1, rely=0.5)

        reg_btn = ttk.Button(self, text="Register", command=lambda: self.register_new_user(parent=self._db))
        reg_btn.place(relheight=0.05, relwidth=0.4, relx=0.3, rely=0.6)

    def register_new_user(self, parent: object) -> None:
        f_name = self.new_first_name_var.get()
        l_name = self.new_last_name_var.get()
        login = self.new_login_var.get()
        password = self.new_pass_var.get()
        if len(f_name) > 0 and len(l_name) > 0 and len(login) > 0 and len(password) > 0:
            if not parent.is_login_taken(login):
                if not parent.is_password_valid(password):
                    parent.create_new_user(f_name, l_name, login, password)
                    print(f"User: {f_name} {l_name} created.")
                    App.switch_frame(self.parent, MainFrame)
                else:
                    self.error_msg.set("Password requirements: minimum 8 characters, at lest 3 digits and 1 upper case.")
            else:
                self.error_msg.set("Login is already taken. Choose another one.")
        else:
            self.error_msg.set("Make sure you filled all fields.")

class SuccessfullLogIn(tk.Frame):
    pass