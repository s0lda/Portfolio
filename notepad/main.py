import tkinter as tk
from tkinter.constants import END, INSERT
from ttkbootstrap import Style
from tkinter import filedialog



class Notepad(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.geometry('500x600')
        self.title('Notepad')
        self.iconbitmap('icon.ico')

        # choose theme for the window
        style = Style(theme= 'pulse')
        self = style.master
        
        
        def open_file():
            file = filedialog.askopenfile(mode= 'r')
            content = file.read()
            text_box.insert(INSERT, content)

        
        def clear_text():
            text_box.delete(1.0, END)


        def save_as():
            file = filedialog.asksaveasfile(mode= 'w', filetypes= [('text file', '*.txt')])
            text = str(text_box.get(1.0, END))
            file.write(text)
            file.close()


        def cut():
            text_box.event_generate("<<Cut>>")


        def copy():
            text_box.event_generate("<<Copy>>")

        
        def paste():
            text_box.event_generate("<<Paste>>")


        # create text box
        text_box = tk.Text(self, height= 35, width= 68, wrap= 'word')
        text_box.place(x= 5, y= 5)

        # create Menu Bar
        menu_bar = tk.Menu(self)
        
        file = tk.Menu(menu_bar)
        file.add_command(label= 'New file', command= clear_text)
        file.add_command(label= 'Open file', command= open_file)
        file.add_command(label= 'Save as', command= save_as)

        menu_bar.add_cascade(label= 'File', menu= file)

        edit = tk.Menu(menu_bar)
        edit.add_command(label= 'Clear', command= clear_text)
        edit.add_command(label= 'Cut', command= cut)
        edit.add_command(label= 'Copy', command= copy)
        edit.add_command(label= 'Paste', command= paste)
        
        menu_bar.add_cascade(label= 'Edit', menu= edit)

        
        self.config(menu = menu_bar)


if __name__ == '__main__':
    Notepad().mainloop()
