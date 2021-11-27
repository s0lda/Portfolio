import os
from scripts.file_manager import FileManager
from scripts.app import App

def main() -> None:
    _res = f'{os.path.dirname(__file__)}\\resources'
    app = App(file_manager=FileManager(), resources=_res)
    app.mainloop()

if __name__ == '__main__':
    main()
