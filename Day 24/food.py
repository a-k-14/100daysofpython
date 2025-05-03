import random
from turtle import Turtle

class Food(Turtle):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        self.shapesize(stretch_wid=0.75, stretch_len=0.75)
        self.x_range = screen_width / 2 - 30
        self.y_range = screen_height / 2 - 30
        self.move()

    def move(self):
        x_pos = random.randint(-self.x_range, self.x_range)
        y_pos = random.randint(-self.y_range, self.y_range)
        self.goto(x=x_pos, y=y_pos)