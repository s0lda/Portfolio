import tkinter as tk
from tkinter import CENTER, ttk, PhotoImage

class ErrorWin(tk.Tk):
    def __init__(self, res_dir: str, screen_size: tuple[int, int], error_type: str) -> None:
        super().__init__()

        self.res = res_dir
        self.error = error_type
        self.title('News Reader ERROR')
        self.iconphoto(True, PhotoImage(file=f'{self.res}//icon.png'))

        self.screen_size = screen_size
        app_win_width = 300
        app_win_height = 150
        app_pos_x = round((self.screen_size[0] / 2) - app_win_width / 2)
        app_pos_y = round((self.screen_size[1] / 2) - app_win_height / 2)
        self.geometry(f"{app_win_width}x{app_win_height}+{app_pos_x}+{app_pos_y}")
        self.resizable(True, True)

        error_lbl = ttk.Label(self, text=self.error, anchor=CENTER)
        error_lbl.place(relheight=0.3, relwidth=0.8, relx=0.1, rely=0.1)

        exit_btn = ttk.Button(self, text='EXIT', command=self.destroy)
        exit_btn.place(relheight=0.2, relwidth=0.5, relx=0.25, rely=0.5)
