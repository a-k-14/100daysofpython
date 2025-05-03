import random
import turtle



class Ball(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        # self.touched_top = False
        # self.touched_right = False
        # self.to_bounce = False
        self.move_x = 10
        self.move_y = 10

    def move(self):
        move_distance = random.randint(1, 10)

        # if not self.touched_top:
        #     move_y = move_distance
        # else:
        #     move_y = -move_distance
        #
        # if not self.touched_right:
        #     move_x = move_distance
        # else:
        #     move_x = -move_distance
        #
        # if self.ycor() >= 250:
        #     self.touched_top = True
        # elif self.ycor() <= -250:
        #     self.touched_top = False
        #
        # if self.xcor() >= 380:
        #     self.touched_right = True
        # elif self.xcor() <= -380:
        #     self.touched_right = False

        # if self.to_bounce:
        #     self.goto(x=self.xcor() + 10, y=self.ycor() - 10)
        # else:
        #     self.goto(x=self.xcor() + 10, y=self.ycor() + 10)

        self.goto(x = self.xcor() + self.move_x, y = self.ycor() + self.move_y)

    def bounce_y(self):
        # self.to_bounce = True
        self.move_y *= -1

    def bounce_x(self):
        self.move_x *= -1

    def reset_pos(self):
        self.goto(0, 0)
        self.bounce_x()

