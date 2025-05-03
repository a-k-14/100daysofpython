from asyncore import write
from turtle import Turtle

class Scoreboard(Turtle):

    def __init__(self, position):
        super().__init__()
        self.color("white")
        self.hideturtle()
        self.penup()
        self.score = 0
        self.setpos(position)
        self.write_score()

    def write_score(self):
        self.clear()
        self.write(arg=f"{self.score}", align="center", font=("Courier", 42, "normal"))

    def update_score(self):
        self.score += 1
        self.write_score()