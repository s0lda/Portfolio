from scr.app import YouTubeDownloader

__version__ = '1.1.1'

def main() -> None:
    print(f'YouTube Downloader v{__version__}')
    YouTubeDownloader().run()

if __name__ == '__main__':
    main()
