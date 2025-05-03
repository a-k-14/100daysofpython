from turtle import Turtle

FONT = ("Courier", 16, "normal")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("black")
        self.level = 1
        self.goto(x=-330, y=200)
        self.write_level()

    def write_level(self):
        self.clear()
        self.write(arg=f"Level: {self.level}", align="left", font=FONT)

    def update_level(self):
        self.level += 1
        self.write_level()

    def game_over(self):
        self.goto(0, 0)
        self.write(arg=f"Game Over", align="center", font=FONT)
