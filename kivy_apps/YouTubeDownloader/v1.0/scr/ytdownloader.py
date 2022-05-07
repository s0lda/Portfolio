from pytube import YouTube

class Downloader:
    def __init__(self, download_path: str) -> None:
        self._d_path = download_path

    def download(self, is_mp3: bool, is_mp4: bool, url: str) -> tuple[str, str]:
        new_name = ''
        try:
            video = YouTube(url)
            name: str = video.title
            print(name)
            # '/', '|' and '\' need to be removed from the name
            # to avoid any OSError's.
            name = name.replace('\\', '').replace('/', '').replace('|', '')
            if is_mp3:
                new_name = f'{name}.mp3'
                print(video.streams.get_audio_only())
                video.streams.get_audio_only().download(filename=new_name, output_path=self._d_path)
            if is_mp4:
                new_name = f'{name}.mp4'
                print(video.streams.get_highest_resolution())
                video.streams.get_highest_resolution().download(filename=new_name, output_path=self._d_path)
        except:
            new_name = 'URL IS INVALID.'
            self._d_path = ''
        return new_name, self._d_path
