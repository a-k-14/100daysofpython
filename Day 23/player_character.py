from turtle import Turtle

class Player(Turtle):
    def __init__(self):
        super().__init__()

        self.shape("turtle")
        self.color("black")
        self.setheading(90)
        self.penup()
        self.goto(x=0, y=-230)

    def move(self):
        if self.ycor() < 230:
            self.forward(20)


class Car(Turtle):
    def __init__(self, y_pos):
        super().__init__()
        self.shape("square")
        self.color("black")
        self.penup()
        self.shapesize(stretch_len=2.5)
        self.goto(x=280, y=y_pos)

    def move(self):
        self.setx(self.xcor() - 10)