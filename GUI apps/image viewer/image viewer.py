from scripts.app import App
import os

def main() -> None:
    _res_path = f'{os.path.dirname(__file__)}/res'
    App(resources=_res_path).mainloop()

if __name__ == '__main__':
    main()
