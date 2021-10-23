import tkinter as tk
from tkinter import PhotoImage, StringVar, ttk
from typing import Any, Union
from sklearn.utils import shuffle
import random, string

class Window(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.geometry('300x300+400+300')
        self.title('Password Generator')
        self.iconphoto(True, PhotoImage(file='icon.png'))
        
        self.length = StringVar(value='0')
        self.letters = StringVar(value='0')
        self.digits = StringVar(value='0')
        self.specials = StringVar(value='0')
        self.password_var = StringVar()

        main_label = ttk.Label(self, text="Please specify requirements for your password.", anchor='center', font=('Arial', 9, 'bold'))
        main_label.place(x=10, y=10, width=280)

        pass_length = ttk.Label(self, text="Password length:")
        pass_length.place(x=10, y=40)

        letters_amount = ttk.Label(self, text="Amount of letters:")
        letters_amount.place(x=10, y=70)

        digits_amount = ttk.Label(self, text="Amount of digits:")
        digits_amount.place(x=10, y=100)

        specials_amount = ttk.Label(self, text="Amount of special characters:")
        specials_amount.place(x=10, y=130)

        length_entry = ttk.Entry(self, textvariable=self.length, justify='right')
        length_entry.place(x=240, y=40, width=50)

        letter_entry = ttk.Entry(self, textvariable=self.letters, justify='right')
        letter_entry.place(x=240, y=70, width=50)

        digits_entry = ttk.Entry(self, textvariable=self.digits, justify='right')
        digits_entry.place(x=240, y=100, width=50)

        specials_entry = ttk.Entry(self, textvariable=self.specials, justify='right')
        specials_entry.place(x=240, y=130, width=50)

        get_pass = ttk.Button(self, text="Generate Password", command=lambda: self.check_for_correct_input(self.length.get(), self.letters.get(), self.digits.get(), self.specials.get()))
        get_pass.place(x=40, y=170, width=220, height=30)

        pass_out = ttk.Entry(self, textvariable=self.password_var, justify='center')
        pass_out.place(x=40, y=220, width=220, height=30)


    def check_for_correct_input(self, length: str, letters: str, digits: str, specials: str) -> Union[None, str]:
        if length.isnumeric() and letters.isnumeric() and digits.isnumeric() and specials.isnumeric():
            self.create_new_password(int(length), int(letters), int(digits), int(specials))
        else:
            self.password_var.set("Check your requirements.")

    def create_new_password(self, length: int, letters: int, digits: int, specials: int) -> None:
        password: list[Any] = []
        if (letters + digits + specials) > length:
            self.password_var.set("Check your requirements.")
        else:
            while letters != 0:
                try:
                    password.append(random.choice(string.ascii_letters))
                    letters -= 1
                finally:
                    pass
            while digits != 0:
                try:
                    password.append(random.randint(0, 9))
                    digits -= 1
                finally:
                    pass
            while specials != 0:
                try:
                    special_signs = ('!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_')
                    password.append(random.choice(special_signs))
                    specials -= 1
                finally:
                    pass

            if len(password) < length:
                difference = length - len(password)
                while difference != 0:
                    try:
                        password.append(random.choice(string.ascii_letters))
                        difference -= 1
                    finally:
                        pass

            password_str: list[str] = [str(i) for i in password]
            password_shuffle: list[str] = shuffle(password_str)
            generated_password = ''.join(password_shuffle)
            self.password_var.set(generated_password)


if __name__ == '__main__':
    Window().mainloop()
