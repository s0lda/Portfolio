from scripts.app import App

def main() -> None:
    _sentences = 'res/sentences.txt'
    App(sentences=_sentences).mainloop()

if __name__ == '__main__':
    main()
