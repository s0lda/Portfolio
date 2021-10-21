import tkinter as tk
from tkinter import PhotoImage, StringVar, ttk
import random


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.geometry('370x220+500+300')
        self.title('Magic 8 Ball')
        self.iconphoto(True, PhotoImage(file='icon.png'))
        self.ans_top_var = StringVar(value="")
        self.answer = StringVar(value="")

        answers = ['It is certain.', 'It is decidedly so.', 'Yes.', 'Reply hazy try again.', 'Ask again later.', 
        'Concentrate and ask again.', 'My reply is no.', 'Outlook not so good.']

        intro_label = ttk.Label(self, text="Please ask the question and press BUTTON for the answer.", anchor='center', font=('Arial', 10))
        intro_label.place(x=10, y=10, height=40, width=350)

        ans_top_label = ttk.Label(self, textvariable=self.ans_top_var, anchor='center', font=('Arial', 10))
        ans_top_label.place(x=10, y=110, height=40, width=350)

        answer_label = ttk.Label(self, textvariable=self.answer, anchor='center', font=('Arial', 10, 'bold'))
        answer_label.place(x= 10, y=160, height=40, width=350)

        answer_button = ttk.Button(self, text="Get the answer", command=lambda: [self.answer.set(random.choice(answers)),
                                                                                 self.ans_top_var.set("THE ANSWER IS:")])
        answer_button.place(x=90, y=60, height=40, width=190)


if __name__ == '__main__':
    App().mainloop()
