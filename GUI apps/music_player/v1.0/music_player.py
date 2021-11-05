import tkinter as tk
from tkinter import ttk
import os
# from ttkbootstrap import Style
import pygame
from tkinter.filedialog import askdirectory


class Music_Player(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.geometry('400x280')
        self.title('Music Player')
        # self.iconbitmap('icon.ico')

        # style = Style(theme= 'darkly')
        # self = style.master

        self.playing_state = False
        self.pause_state = False
        
        # initialize pygame modules for playing the music
        pygame.init()
        pygame.mixer.init()


        # check if it is playing to display right button.
        def is_playing(state: bool):
            if state == False:
                return 'PLAY'
            else:
                return 'STOP'


        def play_list_f():
            directory = askdirectory()
            os.chdir(directory)
            songs = os.listdir()

            for item in songs:
                position = 0
                play_list.insert(position, item)
                position += 1

        
        def play():
            pygame.mixer.music.load(play_list.get(tk.ACTIVE))
            pygame.mixer.music.play()
            self.playing_state = True

        def stop():
            pygame.mixer.music.stop()
            self.playing_state = False

        def pause():
            pygame.mixer.music.pause()
            self.pause_state = True

        def unpause():
            pygame.mixer.music.unpause()
            self.pause_state = False


        def is_pause(state: bool):
            if state == False:
                pause()
            else:
                unpause()

        def play_stop(state: bool):
            if state == False:
                play()
            else:
                stop()


        play_stop_button = ttk.Button(self, text= is_playing(self.playing_state), command= lambda: play_stop(self.playing_state))
        play_stop_button.grid(row= 1, column= 0,  padx= 0, pady= 15, ipadx= 35, ipady= 20)
        
        pause_button = ttk.Button(self, text= '||', command= lambda: is_pause(self.pause_state))
        pause_button.grid(row= 1, column= 1, padx= 0, pady= 15, ipadx= 38, ipady= 20)

        directory_button = ttk.Button(self, text= 'OPEN', command= play_list_f)
        directory_button.grid(row= 1, column= 2,  padx= 0, pady= 15, ipadx= 35, ipady= 20)

        play_list = tk.Listbox(self, width= 57, selectmode= tk.SINGLE)
        play_list.grid(row= 0, column= 0, columnspan= 3)


        # update buttons
        def update():
            play_stop_button['text'] = is_playing(self.playing_state)
            self.after(1000, update)
        update()

if __name__ == "__main__":
    app = Music_Player()
    app.mainloop()
