import tkinter as tk
from tkinter import ACTIVE, END, PhotoImage, StringVar, ttk, font
from scr.news_reader import NewsReader
import webbrowser

class App(tk.Tk):
    def __init__(self, res_dir: str, reader: NewsReader, scree_size: tuple[int, int]) -> None:
        super().__init__()

        self.res = res_dir
        self.reader = reader
        self.title('News Reader')
        self.iconphoto(True, PhotoImage(file=f'{self.res}//icon.png'))

        self.screen_size = scree_size
        app_win_width = 900
        app_win_height = 600
        app_pos_x = round((self.screen_size[0] / 2) - app_win_width / 2)
        app_pos_y = round((self.screen_size[1] / 2) - app_win_height / 2)
        self.geometry(f"{app_win_width}x{app_win_height}+{app_pos_x}+{app_pos_y}")
        self.resizable(True, True)

        self.news_list: list[list[str]] = []

        search_lbl = ttk.Label(self, text='Search:', font=('bold'))
        search_lbl.place(relheight=0.05, relwidth=0.1, relx=0.025, rely=0.01)

        self.search_var = StringVar()
        search_bar = ttk.Entry(self, textvariable=self.search_var)
        search_bar.place(relheight=0.05, relwidth=0.55, relx=0.1, rely=0.01)

        search_btn = ttk.Button(self, text='Search', command=self.display_news)
        search_btn.place(relheight=0.05, relwidth=0.15, relx=0.66, rely=0.01)

        go_to_btn = ttk.Button(self, text='GO TO', command=self.open_link)
        go_to_btn.place(relheight=0.05, relwidth=0.15, relx=0.82, rely=0.01)

        news_box_font = font.Font(family='Helvetica', size=12)
        self.news_box_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.news_box_scrollbar.place(relheight=0.85, relwidth=0.025, relx=0.97, rely=0.07)

        self.news_box = tk.Listbox(self,
                yscrollcommand=self.news_box_scrollbar.set,
                font=news_box_font)
        self.news_box.place(relheight=0.85, relwidth=0.95, relx=0.025, rely=0.07)

        self.news_box_scrollbar.config(command=self.news_box.yview)

        refresh_btn = ttk.Button(self, text='REFRESH', command=self.display_news)
        refresh_btn.place(relheight=0.05, relwidth=0.8, relx=0.1, rely=0.935)
    
        self.display_news()

    def get_news(self, search: str | None) -> None:
        for news in self.reader.read_news(search=search):
            self.news_list.append(news)

    def display_news(self) -> None:
        search = self.search_var.get()
        if search == '':
            self.get_news(search=None)
        else:
            self.get_news(search=search)
        self.news_box.delete(0, END)
        for news in self.news_list:
            position = 0
            self.news_box.insert(position, news[0])
            position += 1

    def open_link(self) -> None:
        for news in self.news_list:
            if self.news_box.get(ACTIVE) == news[0]:
                webbrowser.open(news[1])

