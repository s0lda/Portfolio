import os
from scripts.app import App
from scripts.sorter import Sorter
from pathlib import Path

def main() -> None:
    _home_path = str(Path.home())
    icons_path = f'{os.path.dirname(__file__)}/res'
    _sorter = Sorter(home_path=_home_path)
    app = App(icons_path=icons_path, sorter=_sorter)
    app.mainloop()

if __name__ == '__main__':
    main()
    