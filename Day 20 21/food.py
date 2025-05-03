import turtle
import random

class Food(turtle.Turtle):

    def __init__(self):
        super().__init__()
        # self.food = turtle.Turtle(shape="circle")
        self.shape("circle")
        self.color("blue")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)

        self.refresh()

    def refresh(self):
        random_x = random.randint(-230, 230)
        random_y = random.randint(-230, 230)
        self.goto(random_x, random_y)