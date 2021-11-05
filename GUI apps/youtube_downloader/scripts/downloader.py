from pytube import YouTube
from pathlib import Path

class Downloader:
    def __init__(self) -> None:
        super().__init__()

    def download(self, MP3BoolVal: bool, url: str) -> list[str]:
        downloads_path = str(Path.home() / 'Downloads')
        video = YouTube(url)
        name = video.title
        # / and \ need to be removed from the name. otherwise tkinter calls OSError as it's taking it as part of path
        name = name.replace('\\', '').replace('/', '')
        if MP3BoolVal:
            new_name = f'{name}.mp3'
            print(video.streams.get_audio_only())
            video.streams.get_audio_only().download(filename=new_name, output_path=downloads_path)
        else:
            new_name = f'{name}.mp4'
            print(video.streams.get_highest_resolution())
            video.streams.get_highest_resolution().download(filename=new_name, output_path=downloads_path)

        return [new_name, downloads_path]
        