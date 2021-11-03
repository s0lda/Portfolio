import sys, os
sys.path.append(f'{os.path.dirname(__file__)}\\scripts')
from scripts.app import App
from scripts.downloader import Downloader

def main() -> None:
    _eng = Downloader()
    App(engine=_eng).mainloop()

if __name__ == '__main__':
    main()
