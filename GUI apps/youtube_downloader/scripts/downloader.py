from pytube import YouTube

class Downloader:
    def __init__(self, download_path: str) -> None:
        super().__init__()
        self._d_path = download_path

    def download(self, audio_only: bool, url: str) -> tuple[str, str]:
        
        try:    
            video = YouTube(url)
            name = video.title
            # '/', '|' and '\' need to be removed from the name. 
            # otherwise tkinter calls OSError as it's taking it as a part of path
            name = name.replace('\\', '').replace('/', '').replace('|', '')
            if audio_only:
                new_name = f'{name}.mp3'
                print(video.streams.get_audio_only())
                video.streams.get_audio_only().download(filename=new_name, output_path=self._d_path)
            else:
                new_name = f'{name}.mp4'
                print(video.streams.get_highest_resolution())
                video.streams.get_highest_resolution().download(filename=new_name, output_path=self._d_path)
        except:
            new_name = 'URL IS NOT CORRECT'
            self._d_path = ''

        return new_name, self._d_path
