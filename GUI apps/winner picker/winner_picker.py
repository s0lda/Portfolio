import tkinter as tk
from tkinter import PhotoImage, StringVar, ttk
import random
from tkinter.constants import END, NO


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.geometry('480x400+300+300')
        self.iconphoto(True, PhotoImage(file='icon.png'))
        self.title('Winner Picker')

        self.entry_var = StringVar()
        self.contestant_list: list[str] = []
        self.winner_is = StringVar(value=self.pick_button_f())

        self.create_buttons()
        self.create_labels()
        self.create_list_of_cont()
        self.create_entry()
        


    def create_buttons(self) -> None:
        self.add_button = ttk.Button(self, text='Add', command=self.add_button_f)
        self.add_button.place(x=10, y=140, height=50, width=70)
        self.add_button.invoke()

        pick_button = ttk.Button(self, text='Pick', command=self.pick_button_f)
        pick_button.place(x=90, y=140, height=50, width=70)

        reset_button = ttk.Button(self, text='Reset', command=self.reset_button_f)
        reset_button.place(x=170, y=140, height=50, width=70)


    def create_labels(self) -> None:
        enter_label = ttk.Label(self, text='Enter Contestant:', font=('Arial', 12), anchor='center', background='lightgray')
        enter_label.place(x=10, y=10, width=230)

        winner_ann_label = ttk.Label(self, text='The Winner is:', font=('Arial', 12), anchor='center', background='lightgray')
        winner_ann_label.place(x=10, y=215, width=230)

        winner_label = ttk.Label(self, textvariable=self.winner_is, font=('Arial', 12, 'bold'), anchor='center')
        winner_label.place(x=10, y=245, width=230)


    def create_list_of_cont(self) -> None:
        columns = ('#1')
        self.cont_view = ttk.Treeview(self, columns=columns, show='headings', height=27, selectmode='browse')
        self.cont_view.place(x=260, y=10, width=200, height=380)

        self.cont_view.heading('#1', text='Name')
        self.cont_view.column('#1', anchor='center', stretch=NO, width=198)

        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.cont_view.yview)
        self.cont_view.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=460, y=10, height=380)


    def create_entry(self) -> None:
        self.entry_point = ttk.Entry(self, textvariable=self.entry_var, font=('Arial', 12), justify='center')
        self.entry_point.place(x=10, y=40, height=40, width=230)
        self.entry_point.bind('<Return>', lambda event=None: self.add_button.invoke())
        
        

    def add_button_f(self) -> None:
        if len(self.entry_var.get()) > 0:
            self.contestant_list.append(self.entry_var.get())
            self.cont_view.insert('', tk.END, values=''.join(list((self.entry_var.get()))))
            self.entry_point.delete(0, END)

    
    def reset_button_f(self) -> None:
        self.contestant_list: list[str] = []
        for child in self.cont_view.get_children():
            self.cont_view.delete(child)
        self.winner_is.set('No one yet')

    
    def pick_button_f(self) -> str:
        if len(self.contestant_list) > 0:
            self.winner_is.set(random.choice(self.contestant_list))
        return 'No one yet'




if __name__ == '__main__':
    App().mainloop()
