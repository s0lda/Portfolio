import tkinter as tk
from tkinter import PhotoImage, StringVar, ttk
from PIL import ImageTk, Image
from tkinter.filedialog import askdirectory, askopenfile
import os, filetype
from pathlib import Path

class App(tk.Tk):
    def __init__(self, resources: str) -> None:
        super().__init__()
        self.res = resources

        self.title('Image Viewer')
        self.iconphoto(True, PhotoImage(file=f'{self.res}\\icon.png'))

        self.screensize = self._get_screen_size()
        # Set window size to 75% of the screen size.
        self.width = round((self.screensize[0] / 100) * 75)
        self.height = round((self.screensize[1] / 100) * 75)
        scr_x = round((self.screensize[0] / 2) - (self.width / 2))
        scr_y = round((self.screensize[1] / 2) - (self.height / 2))
        self.geometry(f'{self.width}x{self.height}+{scr_x}+{scr_y}')
        self.resizable(True, True)
        # List to store file paths for open folder option.
        self.file_list: list[str] = []
        # Stringvar to store path of current file.
        self.img_var = StringVar(value=f'{self.res}\\icon.png')
        self.image_index = 0
        self.show_image()


        self.next_btn = ttk.Button(self, text='>>>', command=self.button_next, state='disabled')
        self.next_btn.place(relheight=0.05, relwidth=0.05, relx=0.5, rely=0.92)
        self.prev_btn = ttk.Button(self, text='<<<', command=self.button_previous, state='disabled')
        self.prev_btn.place(relheight=0.05, relwidth=0.05, relx=0.45, rely=0.92)
        open_file = ttk.Button(self, text='Open File', command=lambda: self.open_files('FILE'))
        open_file.place(relheight=0.05, relwidth=0.05, relx=0.8, rely=0.92)
        open_dir = ttk.Button(self, text='Open Folder', command=lambda: self.open_files('DIR'))
        open_dir.place(relheight=0.05, relwidth=0.05, relx=0.85, rely=0.92)

    def _get_screen_size(self) -> tuple[float, float]:
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
        print(f'Monitor: {screen_width}x{screen_height}')
        return screen_width, screen_height

    def show_image(self) -> None:
        _image = Image.open(f'{self.img_var.get()}')
        label_width =  round((self.width / 100) * 98)
        label_height = round((self.height / 100) * 90)
        # Resize image if x,y are bigger than the label.
        # Both parameters have to be bigger for resize, otherwise
        # in some cases images were over streched,
        if _image.size[0] > label_width and _image.size[1] > label_height:
            _image = _image.resize((label_width, label_height), Image.ANTIALIAS)
        self.img_prv = ImageTk.PhotoImage(_image)
        self.image_label = ttk.Label(self, image=self.img_prv, anchor='center')
        self.image_label.place(relheight=0.9, relwidth=0.98, relx=0.01, rely=0.01)

    def open_files(self, file_or_files: str) -> None:
        # Empty list with photo paths.
        self.file_list: list[str] = []
        # Reset image index back to 0.
        self.image_index = 0
        if file_or_files == 'FILE':
            file = askopenfile(initialdir=str(Path.home() / 'Pictures'))
            if filetype.is_image(file.name):
                self.file_list.append(file.name)    
        else:
            directory = askdirectory(initialdir=str(Path.home() / 'Pictures'))
            print(str(Path.home() / 'Images'))
            try:
                os.chdir(directory)
                photos = os.listdir()
                for item in photos:
                    if filetype.is_image(item):
                        self.file_list.append(f'{directory}/{item}')
            except OSError:
                pass
        # Show first image from the list.
        # If list is empty, show App icon.
        if len(self.file_list) == 0:
            self.img_var.set(f'{self.res}/icon.png')
        else:
            self.img_var.set(self.file_list[self.image_index])
        # Refresh image view.
        self.image_label.destroy()
        self.show_image()
        # Activate buttons if there is more than 1 image in collection to view.    
        if len(self.file_list) > 1:
            self.next_btn['state'] = 'normal'
            self.prev_btn['state'] = 'normal'
        else:
            self.next_btn['state'] = 'disabled'
            self.prev_btn['state'] = 'disabled'
    
    def button_next(self) -> None:
        if self.image_index >= 0 and self.image_index < (len(self.file_list) - 1):
            self.image_index += 1
            self.img_var.set(self.file_list[self.image_index])
        else:
            self.image_index = 0
            self.img_var.set(self.file_list[self.image_index])
        # Refresh image view.
        self.image_label.destroy()
        self.show_image()

    def button_previous(self) -> None:
        if self.image_index > 0 and self.image_index <= (len(self.file_list) - 1):
            self.image_index -= 1
            self.img_var.set(self.file_list[self.image_index])
        else:
            self.image_index = len(self.file_list) - 1
            self.img_var.set(self.file_list[self.image_index])
        # Refresh image view.
        self.image_label.destroy()
        self.show_image()
