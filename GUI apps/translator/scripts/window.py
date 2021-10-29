import tkinter as tk
from tkinter import PhotoImage, StringVar, ttk
from typing import Any


class Window(tk.Tk):
    def __init__(self, translator: Any):
        super().__init__()
        self._translator = translator


        self.geometry('250x250+400+300')
        self.title('Translator')
        self.iconphoto(True, PhotoImage(file='icon.png'))

        self.detect_lang_var = StringVar(value='Language')
        detect_lang_lbl = ttk.Label(self, textvariable=self.detect_lang_var, anchor='center')
        detect_lang_lbl.place(x=10, y=10, width=230, height=30)

        self.lang_ent_var = StringVar()
        lang_ent_field = ttk.Entry(self, justify='center', textvariable=self.lang_ent_var)
        lang_ent_field.place(x=10, y=50, width=230, height=30)

        trans_button = ttk.Button(self, text='Translate', command=lambda: [self.detect_lang_var.set(self._translator.detect_lang(self.lang_ent_var.get())),
                                                                            self.out_var.set(self._translator.translate_text(self.lang_ent_var.get(), self._translator.get_lang_code(self.trans_to.get())))])
        trans_button.place(x=10, y=90, width=230, height=30)
        
        list_of_languages = sorted(self._translator.get_lst_of_langs())
        self.trans_to = StringVar()
        lang_options = ttk.OptionMenu(self, self.trans_to,
                                                list_of_languages[19],  # set to English as standard
                                                *list_of_languages)
        lang_options.place(x=10, y=130, width=230, height=30)

        self.out_var = StringVar()
        out_entry = ttk.Entry(self, textvariable=self.out_var, justify='center')
        out_entry.place(x=10, y=170, width=230, height=30)
