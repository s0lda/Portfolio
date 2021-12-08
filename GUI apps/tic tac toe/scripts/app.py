import tkinter as tk
from tkinter import BooleanVar, PhotoImage, StringVar, ttk
import random

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("TIC TAC TOE")
        self.iconphoto(True, PhotoImage(file="icon.png"))
        self.geometry("500x600")
        self.player_turn = BooleanVar(value=True)
        self.player_turn.trace_add("write", self.trace_turn)
        
        self.winner_var = StringVar()
        new_game_btn = ttk.Button(text="NEW GAME", command=lambda: self.game("NEW GAME"))
        new_game_btn.place(relheight=0.1, relwidth=0.8, relx=0.1, rely=0.85)
        self.winner_lbl = ttk.Label(self, textvariable=self.winner_var, anchor='center')
        self.winner_lbl.place(relheight=0.1, relwidth=0.8, relx=0.1, rely=0.75)

        self.btn1 = ttk.Button(self, command=lambda: self.button_click(self.btn1))
        self.btn1.place(relheight=0.2, relwidth=0.3, relx=0.05, rely=0.1)
        self.btn2 = ttk.Button(self, command=lambda: self.button_click(self.btn2))
        self.btn2.place(relheight=0.2, relwidth=0.3, relx=0.35, rely=0.1)
        self.btn3 = ttk.Button(self, command=lambda: self.button_click(self.btn3))
        self.btn3.place(relheight=0.2, relwidth=0.3, relx=0.65, rely=0.1)
        self.btn4 = ttk.Button(self, command=lambda: self.button_click(self.btn4))
        self.btn4.place(relheight=0.2, relwidth=0.3, relx=0.05, rely=0.3)
        self.btn5 = ttk.Button(self, command=lambda: self.button_click(self.btn5))
        self.btn5.place(relheight=0.2, relwidth=0.3, relx=0.35, rely=0.3)
        self.btn6 = ttk.Button(self, command=lambda: self.button_click(self.btn6))
        self.btn6.place(relheight=0.2, relwidth=0.3, relx=0.65, rely=0.3)
        self.btn7 = ttk.Button(self, command=lambda: self.button_click(self.btn7))
        self.btn7.place(relheight=0.2, relwidth=0.3, relx=0.05, rely=0.5)
        self.btn8 = ttk.Button(self, command=lambda: self.button_click(self.btn8))
        self.btn8.place(relheight=0.2, relwidth=0.3, relx=0.35, rely=0.5)
        self.btn9 = ttk.Button(self, command=lambda: self.button_click(self.btn9))
        self.btn9.place(relheight=0.2, relwidth=0.3, relx=0.65, rely=0.5)
        
        self.available_buttons: list[ttk.Button] = [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6, self.btn7, self.btn8, self.btn9]
        self.player_choices: list[ttk.Button] = []
        self.computer_choices: list[ttk.Button] = []
    
    def button_click(self, button: ttk.Button) -> None:
        button["state"] = "disabled"
        self.available_buttons.remove(button)
        if self.player_turn.get():
            button["text"] = "X"
            self.player_choices.append(button)
            if not self.check_winner(self.player_choices):
                self.player_turn.set(False)
        else:
            button["text"] = "O"
            self.computer_choices.append(button)
            if not self.check_winner(self.computer_choices):
                self.player_turn.set(True)        

    def trace_turn(self, name: str, index: str, operation: str) -> None:
        if not self.player_turn.get():
            try:
                computer_choice = random.choice(self.available_buttons)
                self.button_click(computer_choice)
            except IndexError:
                pass

    def game(self, operation: str) -> None:
        btn_list: list[ttk.Button] = [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6, self.btn7, self.btn8, self.btn9]
        if operation == "NEW GAME":
            for item in btn_list:
                item["text"] = ""
                item["state"] = "normal"
            self.player_turn.set(True)
            self.available_buttons = btn_list
            self.player_choices = []
            self.computer_choices = []
            self.winner_var.set("")
        else:
            for item in btn_list:
                item["state"] = "disabled"

    def check_winner(self, current_player: list[ttk.Button]) -> bool:
        winning: list[list[object]] = [
            [self.btn1, self.btn2, self.btn3],
            [self.btn4, self.btn5, self.btn6],
            [self.btn7, self.btn8, self.btn9],
            [self.btn1, self.btn4, self.btn7],
            [self.btn2, self.btn5, self.btn8],
            [self.btn3, self.btn6, self.btn9],
            [self.btn1, self.btn5, self.btn9],
            [self.btn3, self.btn5, self.btn7]
        ]
        for btn_set in winning:
            correct_fields = 0
            for btn in btn_set:
                if btn in current_player:
                    correct_fields += 1
            if correct_fields == 3:
                self.game("END GAME")
                if current_player == self.player_choices:
                    self.winner_var.set("YOU WON!")
                else:
                    self.winner_var.set("COMPUTER WON.")
                return True
        return False
