from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.core.window import Window
import random

class PongPaddle(Widget):
    score = NumericProperty(0)
    
    def bounce_ball(self, ball) -> None:
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.5
            ball.velocity = vel.x, vel.y + offset

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    def move(self) -> None:
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    ball = ObjectProperty(None)
    player = ObjectProperty(None)
    computer = ObjectProperty(None)
    
    def serve_ball(self, vel=(4, 0)) -> None:
        self.ball.center = self.center
        self.ball.velocity = vel
    
    def update(self, dt) -> None:
        self.ball.move()
        self.update_computer_paddle()
        
        self.player.bounce_ball(self.ball)
        self.computer.bounce_ball(self.ball)
        
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        if self.ball.x < self.x:
            print(self.ball.x, self.ball.right)
            self.computer.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            print(self.ball.x, self.ball.right)
            self.player.score += 1
            self.serve_ball(vel=(-4, 0))
        
    def update_computer_paddle(self) -> None:
        self.computer.center_y = self.ball.y

    def on_touch_move(self, touch) -> None:
        if touch.x < self.width / 3:
            self.player.center_y = touch.y

class PongApp(App):
    def build(self) -> Widget:
        Window.size = (800, 600)
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game