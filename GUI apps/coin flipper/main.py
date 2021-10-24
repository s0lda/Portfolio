from scripts.window import Window
from scripts.coinflipper import CoinFlipper
import os

def main() -> None:
    _program = CoinFlipper()
    _icons = f"{os.path.dirname(__file__)}\\icons"
    Window(iconPath=_icons, app=_program).mainloop()

if __name__ == '__main__':
    main()
