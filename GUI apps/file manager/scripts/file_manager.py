import os, shutil, string, subprocess
from pathlib import Path


class FileManager:
    def __init__(self) -> None:
        super().__init__()

    def get_home_path(self) -> str:
        '''Returns home directory.'''
        return str(Path.home())

    def get_drives(self) -> list[str]:
        '''Returns all available drives.'''
        drives: list[str] = []
        for letter in string.ascii_uppercase:
            if os.path.exists(f'{letter}:\\'):
                drives.append(letter)
        return drives

    def get_top_folder(self, current_folder: str) -> str:
        '''Returns the 'mother' path of current directory.'''
        return os.path.split(current_folder)[0]

    def get_file_size(self, file: str) -> int:
        '''Returns size of a file.'''
        try:
            return os.stat(file).st_size
        except:
            return 0

    def get_files_from_dir(self, directory: str) -> list[str]:
        '''Returns list with paths of each item in selected directory.'''
        files: list[str] = []
        try:
            for file in os.listdir(directory):
                files.append(file)
        except NotADirectoryError:
            files.append(directory)
        return files

    def check_if_path_exists(self, path: str) -> bool:
        '''Return True if path is valid, otherwise return False.'''
        return os.path.exists(path)

    def check_if_path_is_directory(self, file_path: str) -> bool:
        '''Check if file is directory. True for folders, False for Files.'''
        if os.path.isdir(file_path):
            return True
        return False

    def get_file_name_from_dir(self, directory: str) -> str:
        '''From path returns final component.'''
        return os.path.basename(directory)

    def remove(self, file_path: str) -> None:
        '''Will remove file or folder(with or without content).'''
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)

    def copy_paste(self, source: str, destination: str) -> None:
        shutil.copy(source, destination)

    def create_new_folder(self, directory: str) -> None:
        '''Will create new folder in specified directory, named: 'New Folder'.'''
        new_folder = f'{directory}\\New Folder'
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
            print(f'New folder have been created in {directory}.')

    def create_new_txt_file(self, directory: str) -> None:
        '''Will create new text file in specified directory, named: 'New Text File.txt'. '''
        try:
            with open(f'{directory}\\New Text File.txt', 'w') as f:
                f.close()
            print(f'New text file have been created in {directory}.')
        except:
            print("Can't create the file. File already exists.")