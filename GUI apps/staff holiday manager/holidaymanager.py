from scripts.app import App
from scripts.database import Database
from pathlib import Path


def main() -> None:
    _documents_path = str(Path.home() / 'Documents')
    _files_path = f'{_documents_path}\\Staff Holiday Manager'
    _db = Database(path=_files_path)
    _res = './res'
    App(database=_db, resources=_res).mainloop()

if __name__ == '__main__':
    main()
