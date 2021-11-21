import os, shutil

class Sorter:
    def __init__(self, home_path: str) -> None:
        super().__init__()
        self.home_path = home_path
        self.downloads_path = f'{self.home_path}\\Downloads'
        print(self.downloads_path)
        self.downloads_folder_content = os.listdir(self.downloads_path)


    def sort_audio(self) -> None:
        '''Find audio files in Downloads and move them to Music.'''
        audio_ext = ('.mp3', '.wma', '.mid', '.m4a', '.ogg', '.flac', '.wav', '.amr')
        audio: list[str] = []
        for file in self.downloads_folder_content:
            extension = os.path.splitext(file)[-1]
            if extension in audio_ext:
                audio.append(file)
        for item in self.downloads_folder_content:
            if item in audio:
                shutil.move(f'{self.downloads_path}\\{item}', f'{self.home_path}\\Music')

    def sort_video(self) -> None:
        '''Find video files in Downloads and move them to Videos.'''
        video_ext = ('3gp', 'mp4', 'm4v', 'mkv', 'webm', 'mov', 'avi', 'wmv', 'mpg', 'flv')
        videos: list[str] = []
        for file in self.downloads_folder_content:
            extension = os.path.splitext(file)[-1]
            if extension in video_ext:
                videos.append(file)
        for item in self.downloads_folder_content:
            if item in videos:
                shutil.move(f'{self.downloads_path}\\{item}', f'{self.home_path}\\Videos')

    def sort_pictures(self) -> None:
        '''Find image files in Downloads and move them to Pictures.'''
        pictures_ext = ('.jpg', '.gif', '.png','.jpx', '.bmp', '.ico', 'dwg', 'xcf', 'webp', 'psd')
        pictures: list[str] = []
        for file in self.downloads_folder_content:
            extension = os.path.splitext(file)[-1]
            if extension in pictures_ext:
                pictures.append(file)
        for item in self.downloads_folder_content:
            if item in pictures:
                shutil.move(f'{self.downloads_path}\\{item}', f'{self.home_path}\\Pictures')

    def sort_documents(self) -> None:
        '''Find document files in Downloads and move them to Documents.'''
        documents_ext = ('.pdf', '.doc', '.docx', '.docm', '.dot', '.dotm', '.dotx', '.html', '.txt', '.xps', 
                        '.csv', '.xls', '.xlsb', '.xlsm', '.xltx', '.xps', '.xml')
        documents: list[str] = []
        for file in self.downloads_folder_content:
            extension = os.path.splitext(file)[-1]
            if extension in documents_ext:
                documents.append(file)
        for item in self.downloads_folder_content:
            if item in documents:
                shutil.move(f'{self.downloads_path}\\{item}', f'{self.home_path}\\Documents')