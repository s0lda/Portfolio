import tkinter as tk
from tkinter import PhotoImage, StringVar, ttk
import random
from functools import partial
from datetime import datetime
from difflib import SequenceMatcher

'''
While typing short sentences, like abcd, float division error may happen. 
Obviously, no point to check typing speed on sentences like this.
They should be made of at least a few words. Therefor I have left it as it is.
'''

class App(tk.Tk):
    def __init__(self, sentences: str):
        super().__init__()

        self.title('Speed Typing Test')
        self.iconphoto(True, PhotoImage(file='icon.png'))
        self.geometry('700x300+400+300')
        self.resizable(True, True)
        self.sentences = sentences
        self.typing_status = False
        self.configure(background="#a2c9f6")

        self.test_sentence = StringVar(value=self.get_sentence())
        self.entry_field = StringVar()
        self.result_var = StringVar()
        self.start = StringVar()
        self.finish = StringVar()

        label = partial(ttk.Label, self, font=('Helvetica', 12, 'bold'), anchor='center', background='#a2c9f6')

        info_lbl = label(text='Start typing to begin, end test with Enter.')
        info_lbl.place(relheight=0.1, relwidth=0.8, relx=0.1, rely=0.1)

        sentence_lbl = label(textvariable=self.test_sentence)
        sentence_lbl.place(relheight=0.1, relwidth=0.8, relx=0.1, rely=0.3)

        self.entry_ent = ttk.Entry(self, textvariable=self.entry_field, justify='center')
        self.entry_ent.place(relheight=0.1, relwidth=0.8, relx=0.1, rely=0.5)

        restart_btn = ttk.Button(self, text='Restart', command=self.restart)
        restart_btn.place(relheight=0.1, relwidth=0.2, relx=0.05, rely=0.8)

        result = label(textvariable=self.result_var)
        result.place(relheight=0.1, relwidth=0.5, relx=0.4, rely=0.8)

        self.entry_ent.bind('<Key>', lambda event: self.check_if_first_click())
        self.entry_ent.bind('<Return>', lambda event: self.check_if_last_click())

    def get_sentence(self) -> str:
        with open(self.sentences, 'r') as f:
            data = f.readlines()
        return random.choice(data)

    def restart(self) -> None:
        self.entry_field.set('')
        self.result_var.set('')
        self.test_sentence.set(self.get_sentence())
        self.typing_status = False
        print('Data reset')

    def check_if_first_click(self) -> None:
        if self.typing_status:
            pass
        else:
            self.typing_status = True
            start_time = datetime.now()
            start_time_str = datetime.strftime(start_time, "%m/%d/%Y, %H:%M:%S")
            self.start.set(start_time_str)
            print('start time set')

    def check_if_last_click(self) -> None:
        if self.typing_status:
            # self.typing_status = False
            finish_time = datetime.now()
            finish_time_str = datetime.strftime(finish_time, "%m/%d/%Y, %H:%M:%S")
            self.finish.set(finish_time_str)
            print('finish time set')
            self.get_result()
        else:
            pass

    def get_result(self) -> None:
        print('getting results')

        finish = self.finish.get()
        start = self.start.get()
        time = datetime.strptime(finish, "%m/%d/%Y, %H:%M:%S") - datetime.strptime(start, "%m/%d/%Y, %H:%M:%S")
        time_min = time.total_seconds() / 60

        gross_WPM = (len(self.test_sentence.get()) / 5) / time_min

        ratio = (SequenceMatcher(None, self.test_sentence.get(), self.entry_ent.get()).ratio()) * 100

        # Sequence matcher does some weird calculations and returned just under 100% during the test
        # when both sentences were exactly the same. Only small difference, but e.g. 99.87 is not a 100. 
        if self.test_sentence.get() == self.entry_ent.get():
            ratio = 100

        result = f'WPM: {round(gross_WPM, 2)} CORRECT: {round(ratio, 2)}'
        self.result_var.set(result)
        print('results done')