import tkinter as tk
from tkinter import ttk
from typing import Any

class Window(tk.Tk):
    def __init__(self, iconPath: str, app: Any) -> None:
        super().__init__()
        self._icon_path = iconPath
        self._app = app

        self.geometry('250x250+400+300')
        self.title('Coin Flipper')
        self.iconphoto(True, tk.PhotoImage(file=f"{self._icon_path}\\head.png"))

        self.ico_img_var = tk.StringVar(value='question')
        self.ico_img_var.trace_add('write', self.update_image)
        self.out_var = tk.StringVar(value="Flip the Coin!")

        self.coin_img = tk.PhotoImage(file=f"{self._icon_path}\\{self.ico_img_var.get()}.png")
        
        self.ico_img_lbl = ttk.Label(self, image=self.coin_img)
        self.ico_img_lbl.place(x=60, y=10, height=130, width=130)

        self.out_lbl = ttk.Label(self, textvariable=self.out_var, anchor='center')
        self.out_lbl.place(x=5, y=150, width=240)

        self.flip_coin = ttk.Button(self, text="Flip the Coin", command=lambda: [self.ico_img_var.set(f'{self._app.flip_the_coin()}'),
                                                                                self.out_var.set(self._app.out_message(self.ico_img_var.get()))])
        self.flip_coin.place(x=75, y=190, width=100)

    # x, y, z required by .trace_add, no arguments passed.
    def update_image(self, x: Any, y: Any, z: Any) -> None:
        self.coin_img = tk.PhotoImage(file=f"{self._icon_path}\\{self.ico_img_var.get()}.png")
        self.ico_img_lbl['image'] = self.coin_img
