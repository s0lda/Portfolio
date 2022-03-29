from kivy.app import App
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from scr.kivyScreenSize import get_screen_size

class Calculator(RelativeLayout):
    memory: str = ''
    operation: str = ''
    
    def on_key_down(self, *args: tuple[object, int, int, str, list[str]]) -> None:
        calc_buttons = ['+', '-', '*', '/', '=', '.', 'C', 'c'
                        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        # Needed to get the keyboard input as kivy
        # doesn't have a way to get the num pad key pressed
        # it returns some character instead
        # enter etc is returned as None
        match args[1]:
            case 13 | 271:
                self.on_click('=')
            case 267:
                self.on_click('/')
            case 268:
                self.on_click('*')
            case 269:
                self.on_click('-')
            case 270:
                self.on_click('+')
            case 99:
                self.on_click('C')
            case 266:
                self.on_click('.')
            case 256:
                self.on_click('0')
            case 257:
                self.on_click('1')
            case 258:
                self.on_click('2')
            case 259:
                self.on_click('3')
            case 260:
                self.on_click('4')
            case 261:
                self.on_click('5')
            case 262:
                self.on_click('6')
            case 263:
                self.on_click('7')
            case 264:
                self.on_click('8')
            case 265:
                self.on_click('9')

        for symbol in calc_buttons:
            if args[3] == symbol:
                self.on_click(symbol)

    
    def on_click(self, input: str) -> None:
        if input == 'C':
            self.ids.screen.text = '0'
        elif input == '+':
            self.operation = '+'
            self.memory = self.ids.screen.text
            self.ids.screen.text = '0'
        elif input == '-':
            self.operation = '-'
            self.memory = self.ids.screen.text
            self.ids.screen.text = '0'
        elif input == '*':
            self.operation = '*'
            self.memory = self.ids.screen.text
            self.ids.screen.text = '0'
        elif input == '/':
            self.operation = '/'
            self.memory = self.ids.screen.text
            self.ids.screen.text = '0'
        elif input == '=':
            result = 0.0
            if self.operation == '+':
                result = float(self.memory) + float(self.ids.screen.text)
            elif self.operation == '-':
                result = float(self.memory) - float(self.ids.screen.text)
            elif self.operation == '*':
                result = float(self.memory) * float(self.ids.screen.text)
            elif self.operation == '/':
                try:
                    result = float(self.memory) / float(self.ids.screen.text)
                except ZeroDivisionError:
                    result = 0.0
            else:
                pass
            if self.operation != '':
                if result.is_integer():
                    self.ids.screen.text = str(int(result))
                else:
                    self.ids.screen.text = str(result)
            self.memory = ''
            self.operation = ''
        elif input == '.':
            if '.' not in self.ids.screen.text:
                self.ids.screen.text += input
            else:
                pass
        else:
            if input == '0' and self.ids.screen.text == '0':
                pass
            else:
                if self.ids.screen.text == '0':
                    self.ids.screen.text = ''
                    self.ids.screen.text += input
                else:
                    self.ids.screen.text += input


class KivyCalc(App):
    def build(self) -> RelativeLayout:
        screen_size: tuple[int, int] | None = get_screen_size(appsize=False)
        if screen_size != None:
            Window.size = (400, 600)
        Window.clearcolor = (103/255.0, 105/255.0, 111/255.0, 0.3)
        self.title = 'Kivy Calculator'
        self.icon = './res/icon.png'
        _app = Calculator()
        Window.bind(on_key_down=_app.on_key_down)
        return _app
