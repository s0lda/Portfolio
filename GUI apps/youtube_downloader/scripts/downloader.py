from pytube import YouTube
from pathlib import Path

class Downloader:
    def __init__(self) -> None:
        super().__init__()

    def download(self, MP3BoolVal: bool, url: str) -> list[str]:
        downloads_path = str(Path.home() / 'Downloads')
        video = YouTube(url)
        name = video.title
        if MP3BoolVal == True:
            new_name = f'{name}.mp3'
            video.streams.filter(only_audio=MP3BoolVal).first().download(filename=new_name, output_path=downloads_path)
        else:
            new_name = f'{name}.mp4'
            # try to download 720p if not available download whatever is available
            try:
                video.streams.filter(progressive=True, res='720p').first().download(filename=new_name, output_path=downloads_path)
            except AttributeError:
                video.streams.filter(progressive=True).first().download(filename=new_name, output_path=downloads_path)

        return [new_name, downloads_path]
        