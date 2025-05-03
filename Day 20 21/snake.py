import random
import turtle

NUMBER_OF_TURTLES = 3
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

class Snake:

    def __init__(self):
        self.my_turtles = []
        self.create_snake()
        self.head = self.my_turtles[0]

    def create_snake(self):
        x_pos = 0
        for _ in range(0, NUMBER_OF_TURTLES):
            self.add_segment((x_pos, 0))
            x_pos -= 20

    def add_segment(self, position):
        t = turtle.Turtle(shape="square")
        t.color("white")
        t.penup()
        t.setpos(position)
        self.my_turtles.append(t)

    def move(self):
        # for loop runs for 2, 1
        for i in range(len(self.my_turtles) - 1, 0, -1):
            self.my_turtles[i].setpos(self.my_turtles[i - 1].pos())
        self.head.forward(MOVE_DISTANCE)

    def up(self):
        # to prevent going down by reversing the head
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)

    def extend_snake(self):
        # colors = ["violet", "indigo", "blue", "green", "gold", "orange", "red"]
        # t = turtle.Turtle(shape="square")
        # t.color(random.choice(colors))
        # t.penup()
        # x_pos = self.my_turtles[len(self.my_turtles) - 1].xcor()
        # y_pos = self.my_turtles[len(self.my_turtles) - 1].ycor()
        # t.setpos(x=x_pos, y = y_pos)
        # self.my_turtles.append(t)
        # print(len(self.my_turtles))
        tail_position = self.my_turtles[-1].pos()
        self.add_segment(tail_position)

    def check_collision(self):
        # snake_size = len(self.my_turtles)
        # if snake_size = 6
        # range = 0 - 5
        # for loop runs 0 - 4
        # for i in range(snake_size - 1):
        #     if self.head.distance(self.my_turtles[i + 1]) < 10:
        #         return True

        # using slicing
        # get the snake segments excluding the head segment
        tail_segment = self.my_turtles[1:]
        for segment in tail_segment:
            if self.head.distance(segment) < 10:
                return True

        return False