import math
import tkinter as tk
import random
from tkinter import Frame, PhotoImage, Radiobutton, StringVar, ttk
from typing import Any


class Game(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.geometry('400x440+400+300')
        self.title('Guess The Number')
        self.iconphoto(True, PhotoImage(file='icon.png'))

        self.level_var = StringVar(value='medium')
        self.player_var = StringVar(value='Player')
        self.number_var = StringVar(value='0')
        self.player_attempts = 0
        self.computer_attempts = 0
        self.turn = StringVar(value='0')
        self.winner = ''

        self.switch_frame(StartFrame)

    def switch_frame(self, frameClass: Any) -> None:
        new_frame: Frame = frameClass(self)
        self._frame = new_frame
        self._frame.place(x=0, y=0, width=400, height=440)
    
    # function to ensure user input is actually a number nothing else.
    def is_number(self, valueToCheck: str) -> int:
        try:
            return int(valueToCheck)
        except ValueError:
            return 0

    # difficulty level scope
    def game_level(self, level: str) -> int:
        if level == 'low':
            return 10
        elif level == 'medium':
            return 100
        else:
            return 1000
    
    def new_game(self) -> None:
        self.player_attempts = 0
        self.computer_attempts = 0
        self.turn.set('0')
        self.winner = ''

       
class StartFrame(tk.Frame):
    def __init__(self, master: Game) -> None:
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='#9aaeb6')
        main_font = ('Arial', 12, 'bold')
        secondary_font = ('Arial', 10)
        
        main_label = ttk.Label(self, text='Game Settings', anchor='center', background='#eee', font=main_font)
        main_label.place(x=10, y=10, width=380, height=30)

        level_label = ttk.Label(self, text='Difficulty Level', anchor='center', background='#eee', font=secondary_font)
        level_label.place(x=10, y=70, width=380, height=30)

        level_1 = Radiobutton(self, text='Low', variable=master.level_var, value='low')
        level_1.place(x=50, y=110, height=30, width=80)

        level_2 = Radiobutton(self, text='Medium', variable=master.level_var, value='medium')
        level_2.place(x=160, y=110, height=30, width=80)

        level_3 = Radiobutton(self, text='Hard', variable=master.level_var, value='hard')
        level_3.place(x=270, y=110, height=30, width=80)

        player_label = ttk.Label(self, text='Who will start the game? You or Computer?', anchor='center', background='#eee', font=secondary_font)
        player_label.place(x=10, y=150, width=380, height=30)

        player_1 = Radiobutton(self, text='Player', variable=master.player_var, value='Player')
        player_1.place(x=100, y=190, height=30, width=80)

        player_2 = Radiobutton(self, text='Computer', variable=master.player_var, value='Computer')
        player_2.place(x=220, y=190, height=30, width=80)

        number_label = ttk.Label(self, text='What is your secret number?', anchor='center', background='#eee', font=secondary_font)
        number_label.place(x=10, y=230, width=380, height=30)

        number_entry = ttk.Entry(self, textvariable=master.number_var, justify='center')
        number_entry.place(x=100, y=270, width=200, height=40)

        play_button = ttk.Button(self, text='PLAY', command=lambda: master.switch_frame(GameFrame))
        play_button.place(x=100, y=350, width=200, height=60)


class GameFrame(tk.Frame):
    def __init__(self, master: Game) -> None:
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='#9aaeb6')

        main_font = ('Arial', 12, 'bold')
        secondary_font = ('Arial', 10)

        self.com_out = StringVar(value='Let\'s start.')

        if master.player_var.get() == 'Computer':
            master.turn.set('1')
            
        self.player_secret_number = master.is_number(master.number_var.get())
        game_lvl = master.game_level(master.level_var.get())
        self.computer_secret_number = random.randint(0, game_lvl)

        self.computer_low = 0
        self.computer_high = game_lvl

        # ensure player number can't be higher than choosen difficulty lvl scope
        if self.player_secret_number > game_lvl:
            self.player_secret_number = random.randint(0, game_lvl)

        main_label = ttk.Label(self, text='Game Time', anchor='center', background='#eee', font=main_font)
        main_label.place(x=10, y=10, width=380, height=30)

        turn_label = ttk.Label(self, text='Turn:', anchor='center', background='#eee', font=main_font)
        turn_label.place(x=10, y=60, width=190, height=30)

        self.turn_display = StringVar(value='1')
        turn_label_val = ttk.Label(self, textvariable=self.turn_display, anchor='center', background='#eee', font=main_font)
        turn_label_val.place(x=200, y=60, width=190, height=30)

        player_label = ttk.Label(self, text='Player', anchor='center', background='#eee', font=main_font)
        player_label.place(x=50, y=105, width=100, height=30)

        computer_label = ttk.Label(self, text='Computer', anchor='center', background='#eee', font=main_font)
        computer_label.place(x=250, y=105, width=100, height=30)

        command_out = ttk.Label(self, textvariable=self.com_out, anchor='center', font=secondary_font)
        command_out.place(x=115, y=180, height=40, width=180)

        self.player_guess = StringVar()
        player_guess_entry = ttk.Entry(self, textvariable=self.player_guess, justify='center', font=main_font)
        player_guess_entry.place(x=160, y=250, height=40, width=90)

        guess_button = ttk.Button(self, text='Guess', command=lambda: self.play(master=master))
        guess_button.place(x=160, y=300, height=60, width=90)

    def play(self, master: Game) -> None:
        if int(master.turn.get()) % 2 != 0:
            computer_choice = random.randint(self.computer_low, self.computer_high)
            if computer_choice == self.player_secret_number:
                master.winner = 'computer'
                master.switch_frame(WinnerFrame)
            else:
                if computer_choice > self.player_secret_number:
                    self.computer_high = computer_choice
                else:
                    self.computer_low = computer_choice

            master.computer_attempts += 1
            master.turn.set(str(int((master.turn.get())) + 1))
            self.turn_display.set(str(math.ceil(int(master.turn.get()) / 2)))
        else:
            try:    
                player_choice = int(self.player_guess.get())
                if player_choice == self.computer_secret_number:
                    master.winner = 'player'
                    master.switch_frame(WinnerFrame)
                else:
                    if player_choice > self.computer_secret_number:
                        self.com_out.set('Number too high.')
                    else:
                        self.com_out.set('Number too low.')
            except ValueError:
                pass
            
            master.player_attempts += 1
            master.turn.set(str(int((master.turn.get())) + 1))
            self.player_guess.set('0')
            self.turn_display.set(str(math.ceil(int(master.turn.get()) / 2)))
            self.play(master)


class WinnerFrame(tk.Frame):
    def __init__(self, master: Game) -> None:
        tk.Frame.__init__(self, master)
        main_font = ('Arial', 12, 'bold')
        
        def winner_loser():
            if master.winner == 'computer':
                return 'red'
            else:
                return 'green'

        self.configure(background=winner_loser())
        main_label = ttk.Label(self, text='Do you want to play again?', anchor='center', background='#eee', font=main_font)
        main_label.place(x=10, y=120, width=380, height=30)

        yes_button = ttk.Button(self, text='YES', command=lambda: [master.switch_frame(StartFrame),
                                                                    master.new_game()])
        yes_button.place(x=100, y=180, width=90, height=70)

        no_button = ttk.Button(self, text='NO', command=master.destroy)
        no_button.place(x=200, y=180, width=90, height=70)

        def attempt_result() -> str:
            if master.winner == 'computer':
                return f'{master.computer_attempts} moves for Computer to beat you.'
            else:
                return f'{master.player_attempts} moves, all you needed to win.'
        
        result_label = ttk.Label(self, text=attempt_result(), anchor='center')
        result_label.place(x=10, y=270, width=380)

if __name__ == '__main__':
    Game().mainloop()
