from unittest import result
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout

from scr.kivyScreenSize import get_screen_size


class Calculator(RelativeLayout):
    memory = ''
    operation = ''
    
    def on_click(self, input: str) -> None:
        if input == 'C':
            self.ids.screen.text = ''
        elif input == '+':
            self.operation = '+'
            self.memory = self.ids.screen.text
            self.ids.screen.text = ''
        elif input == '-':
            self.operation = '-'
            self.memory = self.ids.screen.text
            self.ids.screen.text = ''
        elif input == '*':
            self.operation = '*'
            self.memory = self.ids.screen.text
            self.ids.screen.text = ''
        elif input == '/':
            self.operation = '/'
            self.memory = self.ids.screen.text
            self.ids.screen.text = ''
        elif input == '=':
            if self.operation == '+':
                result = float(self.memory) + float(self.ids.screen.text)
            elif self.operation == '-':
                result = float(self.memory) - float(self.ids.screen.text)
            elif self.operation == '*':
                result = float(self.memory) * float(self.ids.screen.text)
            elif self.operation == '/':
                result = float(self.memory) / float(self.ids.screen.text)
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
        return Calculator()
