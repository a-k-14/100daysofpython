from turtle import Turtle

# distance in pixels the paddle has to move when we press up/down
MOVEMENT = 20

class Paddle(Turtle):

    def __init__(self, position):
        super().__init__()
        self.shape("square")
        # paddle size is 100 x 20
        # self.shapesize(stretch_len=4)
        self.shapesize(stretch_wid=4, stretch_len=1)
        self.color("white")
        # self.setheading(90)
        self.penup()
        self.goto(position)

    def up(self):
        if self.ycor() <= 200:
            # self.forward(MOVEMENT)
            self.goto(x=self.xcor(), y=self.ycor() + 20)

    def down(self):
        if self.ycor() >= -200:
            # self.backward(MOVEMENT)
            self.goto(x=self.xcor(), y=self.ycor() - 20)
