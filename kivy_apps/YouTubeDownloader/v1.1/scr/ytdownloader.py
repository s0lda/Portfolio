from pytube import YouTube
from pytube.cli import Stream
import os

class Downloader:
    def __init__(self, download_path: str) -> None:
        self._d_path = download_path
        self.bytes_received = 0
        self.file_size = 0

    def download(self, is_mp3: bool, is_mp4: bool, url: str) -> tuple[str, str]:
        '''
        Will process the download of the file.
        Returns the name of the file and the path to the file or an error message:
        'Error. Download failed.'
        '''
        
        new_name = ''
        try:
            video = YouTube(url=url, on_progress_callback=self.on_progress)
            name: str = video.title
            print(name)
            # '/', '|' and '\' need to be removed from the name
            # to avoid any OSError's.
            name = name.replace('\\', '').replace('/', '').replace('|', '')
            if is_mp3:
                new_name = self.check_file_exists(self._d_path, name, '.mp3')
                print(video.streams.get_audio_only())
                video.streams.get_audio_only().download(filename=new_name,
                                                        output_path=self._d_path)
            if is_mp4:
                new_name = self.check_file_exists(self._d_path, name, '.mp4')
                print(video.streams.get_highest_resolution())
                video.streams.get_highest_resolution().download(filename=new_name,
                                                                output_path=self._d_path)
            if is_mp3 and is_mp4:
                new_name = f'{name}  .mp3 .mp4'
        except:
            new_name = 'Error. Download failed.'
            self._d_path = ''
        return new_name, self._d_path
    
    def check_file_exists(self, path: str, name: str, suffix: str) -> str:
        '''
        Checks if the file exists in the directory. If it does, 
        it will add '#' to the name.
        It is to prevent overwriting of files. 
        A lot of YouTube videos have the same name.
        Although the name is the same, the files are different. 
        Using copy(1) would not be suitable in this case.
        '''
        
        file_to_check = f'{path}/{name}{suffix}'
        if os.path.exists(file_to_check):
            return f'{name}#{suffix}'
        return f'{name}{suffix}'

    def on_progress(self, stream: Stream, chunk: bytes, bytes_remaining: int) -> None:
        '''Callback for downloader. Will set downloaded file size and progress.'''
        self.file_size = stream.filesize
        bytes_received = self.file_size - bytes_remaining
        self.bytes_received = bytes_received
    
    def get_bytes_received(self) -> int:
        '''Returns the number of bytes received.'''
        return self.bytes_received
    
    def get_file_size(self) -> int:
        '''Return size of the file to download.'''
        return self.file_size
