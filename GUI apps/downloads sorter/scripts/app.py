import tkinter as tk
from tkinter import BooleanVar, PhotoImage, StringVar, ttk
from scripts.sorter import Sorter

class App(tk.Tk):
    def __init__(self, icons_path: str, sorter: Sorter) -> None:
        super().__init__()
        self.icons = icons_path
        self._sorter = sorter

        self.title('Downloads Sorter')
        self.iconphoto(True, PhotoImage(file=f'{self.icons}/icon.png'))

        self.screensize = self._get_screen_size()
        app_width = round((self.screensize[0] / 100) * 20)
        app_height = round((self.screensize[1] / 100) * 20)
        app_x_pos = round((self.screensize[0] / 2) - (app_width / 2))
        app_y_pos = round((self.screensize[1] / 2) - (app_height / 2))
        self.geometry(f'{app_width}x{app_height}+{app_x_pos}+{app_y_pos}')
        self.resizable(True, True)

        self.Audio = BooleanVar(value=False)
        self.Video = BooleanVar(value=False)
        self.Pictures = BooleanVar(value=False)
        self.Documents = BooleanVar(value=False)
        self.progress_var = StringVar(value='')

        main_lbl = ttk.Label(self, text='Choose file types in your DOWNLOADS to sort.', font=('Helvetica', 10, 'bold'), anchor='center')
        main_lbl.place(relwidth=0.8, relheight=0.1, relx=0.1, rely=0.05)

        audio_check = ttk.Checkbutton(self, text='Music', onvalue=True, offvalue=False, variable=self.Audio)
        audio_check.place(relwidth=0.15, relheight=0.1, relx=0.1, rely=0.15)
        video_check = ttk.Checkbutton(self, text='Videos', onvalue=True, offvalue=False, variable=self.Video)
        video_check.place(relwidth=0.15, relheight=0.1, relx=0.3, rely=0.15)
        pictures_check = ttk.Checkbutton(self, text='Pictures', onvalue=True, offvalue=False, variable=self.Pictures)
        pictures_check.place(relwidth=0.15, relheight=0.1, relx=0.5, rely=0.15)
        documents_check = ttk.Checkbutton(self, text='Documents', onvalue=True, offvalue=False, variable=self.Documents)
        documents_check.place(relwidth=0.15, relheight=0.1, relx=0.7, rely=0.15)

        sort_btn = ttk.Button(self, text='Sort Files', command=self.sort_files)
        sort_btn.place(relwidth=0.3, relheight=0.15, relx=0.35, rely=0.30)
        finished_lbl = ttk.Label(self, textvariable=self.progress_var, font=('Helvetica', 10, 'bold'), anchor='center')
        finished_lbl.place(relwidth=0.8, relheight=0.1, relx=0.1, rely=0.5)

    def sort_files(self) -> None:
        self.progress_var.set('Sorting your Files.')
        if self.Audio.get():
            self._sorter.sort_audio()
        if self.Video.get():
            self._sorter.sort_video()
        if self.Pictures.get():
            self._sorter.sort_pictures()
        if self.Documents.get():
            self._sorter.sort_documents()
        self.progress_var.set('Finished sorting your Files.')

    def _get_screen_size(self) -> tuple[float, float]:
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
        print(f'Monitor: {screen_width}x{screen_height}')
        return screen_width, screen_height
