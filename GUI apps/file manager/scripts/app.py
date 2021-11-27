import tkinter as tk
from tkinter import PhotoImage, StringVar, ttk
from tkinter.constants import NO
from typing import Union
from scripts.file_manager import FileManager

class App(tk.Tk):
    def __init__(self, file_manager: FileManager, resources: str) -> None:
        super().__init__()
        self.f_m = file_manager
        self.res = resources
        self.icon_folder = f'{self.res}\\icons'
        self.current_directory = StringVar(value=self.f_m.get_home_path())
        self.temp_copy_file = ''
        self.cut_bool = False
        
        self.title('File Manager')
        self.iconphoto(True, PhotoImage(file=f'{self.res}\\icon.png'))
        self.screensize = self._get_screen_size()
        # Set window size to 40% of the screen size.
        self.width = round((self.screensize[0] / 100) * 40)
        self.height = round((self.screensize[1] / 100) * 40)
        scr_x = round((self.screensize[0] / 2) - (self.width / 2))
        scr_y = round((self.screensize[1] / 2) - (self.height / 2))
        self.geometry(f'{self.width}x{self.height}+{scr_x}+{scr_y}')
        self.resizable(True, True)

        self.set_menu_bar()
        self.create_menu_icon_bar()
        self.create_side_view_tree()
        self.create_main_view_tree()
        
        go_back_dir_btn = ttk.Button(self, text='<<<',
                                           command=self.go_back_btn_command)
        go_back_dir_btn.place(relheight=0.05, relwidth=0.05, relx=0, rely=0.12)
        next_folder_btn = ttk.Button(self, text='>>>',
                                           command=self.forward_btn_command)
        next_folder_btn.place(relheight=0.05, relwidth=0.05, relx=0.1, rely=0.12)
        home_dir_btn = ttk.Button(self, text='HOME', 
                                        command=lambda: self.current_directory.set(self.f_m.get_home_path()))
        home_dir_btn.place(relheight=0.05, relwidth=0.05, relx=0.05, rely=0.12)
        # Using Entry for easy path copying.
        path_lbl = ttk.Entry(self, textvariable=self.current_directory, justify='left')
        path_lbl.place(relheight=0.05, relwidth=0.85, relx=0.15, rely=0.12)
        self.current_directory.trace_add('write', self.trace_current_dir)

    def _get_screen_size(self) -> tuple[float, float]:
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
        print(f'Monitor: {screen_width}x{screen_height}')
        return screen_width, screen_height

    def set_menu_bar(self) -> None:
        menu_bar = tk.Menu(self)

        file = tk.Menu(menu_bar, 
                       tearoff=False, 
                       font=('Helvetica', 10))
        file.add_command(label='New Folder', 
                         command=self.create_folder)
        file.add_command(label='New Text File',
                         command=self.create_text_file)
        file.add_separator()
        file.add_command(label='Delete',
                         command=self.remove_btn_command)
        
        edit = tk.Menu(menu_bar, 
                       tearoff=False, 
                       font=('Helvetica', 10))
        edit.add_command(label='Copy',
                         command=self.copy_btn_command)
        edit.add_command(label='Cut',
                         command=self.cut_btn_command)
        edit.add_command(label='Paste',
                         command=self.paste_btn_command)

        menu_bar.add_cascade(label='File', menu=file)
        menu_bar.add_cascade(label='Edit', menu=edit)
        self.config(menu=menu_bar)

    def create_menu_icon_bar(self) -> None:
        self.folder_img = PhotoImage(file=f'{self.icon_folder}\\folder.png')
        self.new_doc_img = PhotoImage(file=f'{self.icon_folder}\\new_doc.png')
        self.copy_img = PhotoImage(file=f'{self.icon_folder}\\copy.png')
        self.cut_img = PhotoImage(file=f'{self.icon_folder}\\cut.png')
        self.paste_img = PhotoImage(file=f'{self.icon_folder}\\paste.png')
        self.delete_img = PhotoImage(file=f'{self.icon_folder}\\cancel.png')

        folder_btn = ttk.Button(self, image=self.folder_img,
                                      command=self.create_folder)
        folder_btn.place(relheight=0.12, relwidth=0.1, relx=0, rely=0)
        new_doc_btn = ttk.Button(self, image=self.new_doc_img,
                                       command=self.create_text_file)
        new_doc_btn.place(relheight=0.12, relwidth=0.1, relx=0.1, rely=0)
        copy_btn = ttk.Button(self, image=self.copy_img,
                                    command=self.copy_btn_command)
        copy_btn.place(relheight=0.12, relwidth=0.1, relx=0.23, rely=0)
        cut_btn = ttk.Button(self, image=self.cut_img,
                                   command=self.cut_btn_command)
        cut_btn.place(relheight=0.12, relwidth=0.1, relx=0.33, rely=0)
        paste_btn = ttk.Button(self, image=self.paste_img,
                                     command=self.paste_btn_command)
        paste_btn.place(relheight=0.12, relwidth=0.1, relx=0.43, rely=0)
        delete_btn = ttk.Button(self, image=self.delete_img,
                                      command=self.remove_btn_command)
        delete_btn.place(relheight=0.12, relwidth=0.1, relx=0.53, rely=0)

    def create_side_view_tree(self) -> None:
        columns = ('#1')
        side_panel = ttk.Treeview(self, columns=columns, show='headings', selectmode='none')
        side_panel.place(relheight=0.82, relwidth=0.2, relx=0, rely=0.17)
        side_panel.heading('#1', text='This Computer', anchor='w')
        for item in self.f_m.get_drives():
            side_panel.insert('', tk.END, values=item)

    def create_main_view_tree(self) -> None:
        panel_width = (self.width / 100) * 80
        columns = ('#1', '#2')
        self.main_panel = ttk.Treeview(self, columns=columns, show='headings', selectmode='browse')
        self.main_panel.place(relheight=0.82, relwidth=0.794, relx=0.201, rely=0.17)
        self.main_panel.heading('#1', text='Name')
        self.main_panel.heading('#2', text='Size')
        col_1_width = round(panel_width / 100) * 75
        col_2_width = round(panel_width / 100) * 24
        self.main_panel.column('#1', stretch=NO, width=col_1_width)
        self.main_panel.column('#2', stretch=NO, width=col_2_width)
        for file in self.f_m.get_files_from_dir(self.current_directory.get()):
            name = self.f_m.get_file_name_from_dir(file)
            size = self.f_m.get_file_size(f'{self.current_directory.get()}\\{file}')
            self.main_panel.insert('', tk.END, values=(name, size))
        
    def go_back_btn_command(self) -> None:
        up_path = self.f_m.get_top_folder(self.current_directory.get())
        self.current_directory.set(up_path)

    def forward_btn_command(self) -> None:
        file_name = self.get_focus_from_main_panel()
        if file_name != None:
            new_path = f'{self.current_directory.get()}\\{file_name}'
            if self.f_m.check_if_path_is_directory(new_path):
                self.current_directory.set(new_path)

    def trace_current_dir(self, name: str, index: str, operation: str) -> None:
        self.main_panel.destroy()
        self.create_main_view_tree()

    def remove_btn_command(self) -> None:
        file_name = self.get_focus_from_main_panel()
        if file_name != None:
            new_path = f'{self.current_directory.get()}\\{file_name}'
            self.f_m.remove(new_path)
            self.trace_current_dir('name', 'index', 'operation')

    def create_folder(self) -> None:
        self.f_m.create_new_folder(self.current_directory.get())
        self.trace_current_dir('name', 'index', 'operation')

    def create_text_file(self) -> None:
        self.f_m.create_new_txt_file(self.current_directory.get())
        self.trace_current_dir('name', 'index', 'operation')

    def get_focus_from_main_panel(self) -> Union[str, None]:
        try:
            current_file = self.main_panel.focus()
            file_info = self.main_panel.item(current_file)
            file_name: str = file_info["values"][0]
            print(file_name)
            return file_name
        except IndexError:
            return None

    def copy_btn_command(self) -> None:
        file = self.get_focus_from_main_panel()
        if file != None:
            path = f'{self.current_directory.get()}\\{file}'
            self.temp_copy_file = path

    def paste_btn_command(self) -> None:
        if self.f_m.check_if_path_exists(self.temp_copy_file):
            self.f_m.copy_paste(self.temp_copy_file, self.current_directory.get())
            if self.cut_bool:
                self.f_m.remove(self.temp_copy_file)
                self.cut_bool = False
        self.trace_current_dir('name', 'index', 'operation')

    def cut_btn_command(self) -> None:
        file = self.get_focus_from_main_panel()
        if file != None:
            path = f'{self.current_directory.get()}\\{file}'
            self.temp_copy_file = path
            self.cut_bool = True