import tkinter as tk
from tkinter import BooleanVar, PhotoImage, StringVar, ttk
from functools import partial
from scripts.downloader import Downloader

class App(tk.Tk):
    def __init__(self, engine: Downloader) -> None:
        super().__init__()
        self._eng = engine

        self.title('Youtube Downloader')
        self.iconphoto(True, PhotoImage(file='icon.png'))
        self.geometry('700x300+400+300')
        self.resizable(False, False)
        self.configure(background='#333333')
        self.style = ttk.Style()
        self.style.configure('TCheckbutton', background='#333333', foreground='white')
        self.style.configure('TButton', font=('Tahoma', 10, 'bold'), background='#333333')

        self.link_var = StringVar()
        self.mp3_var = BooleanVar()
        self.file_name = StringVar()
        self.file_path = StringVar()
        # partial used for labels instead of style as it is minimazing code to variable name and text only
        label = partial(ttk.Label, self, font=('Tahoma', 10, 'bold'), background='#333333', foreground='white')

        link_label = label(text='Enter URL:')
        link_label.place(x=10, y=10)
        link_entry = ttk.Entry(self, textvariable=self.link_var)
        link_entry.place(x=10, y=40, width=680, height=30)
        label_mp3 = label(text='Download as MP3:')
        label_mp3.place(x=10, y=75)
        mp3_check = ttk.Checkbutton(self, variable=self.mp3_var, text='MP3', onvalue=True, offvalue=False, style='TCheckbutton')
        mp3_check.place(x=150, y=75)
        download_button = ttk.Button(self, text='DOWNLOAD', style='TButton', command=self._download)
        download_button.place(x=250, y=110, width=200, height=40)
        file_info_label = label(text='File:')
        file_info_label.place(x=10, y=200, height=30)
        file_info_label_var = label(textvariable=self.file_name)
        file_info_label_var.place(x=40, y=200, height=30)
        path_info_label = label(text='Downloaded to:')
        path_info_label.place(x=10, y=240, height=30)
        path_info_label_var = label(textvariable=self.file_path)
        path_info_label_var.place(x=120, y=240, height=30)
        
        self.file_path.trace_add('write', self.empty_entry_field)

    def empty_entry_field(self, name: str, index: str, mode: str) -> None:
        self.link_var.set('')

    def _download(self) -> None:
        url = self.link_var.get()
        as_mp3 = self.mp3_var.get()

        filename, path = self._eng.download(as_mp3, url)

        self.file_name.set(filename)
        self.file_path.set(path)
