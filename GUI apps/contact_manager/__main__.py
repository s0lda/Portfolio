import sys, os
sys.path.append(f'{os.path.dirname(__file__)}\\scripts')
sys.path.append(f'{os.path.dirname(__file__)}\\icons')
from scripts.app import App
from scripts.work import ContactDB

def main() -> None:
    _db = ContactDB(database='settings\\contacts.json')
    App(database=_db).mainloop()

if __name__ == '__main__':
    main()
