from scr.app import App
from scr.usr import User

def main() -> None:
    db_path = f".\\data"
    usr = User(db_path=db_path)
    app = App(user_db=usr)
    app.mainloop()
    
if __name__ == "__main__":
    main()
