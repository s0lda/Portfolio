from scr.application import Application

def main() -> None:
    _resources = './res/'
    _app = Application(resources=_resources)
    _app.run()

if __name__ == '__main__':
    main()
