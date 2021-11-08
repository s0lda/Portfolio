from scripts.app import App
from scripts.downloader import Downloader
from pathlib import Path

def main() -> None:
    _d_path = str(Path.home() / 'Downloads')
    _eng = Downloader(download_path=_d_path)
    App(engine=_eng).mainloop()

if __name__ == '__main__':
    main()
