import random
from turtle import Turtle

BASE_SNAKE_SIZE = 3
COLORS = ["violet", "indigo", "blue", "green", "gold", "orange", "red"]

class Snake:
    def __init__(self):
        self.snake = []
        self.create_snake()
        self.head = self.snake[0]

    # create the initial snake body
    def create_snake(self):
        for _ in range(0, BASE_SNAKE_SIZE):
            self.add_segment()

    # to create individual segments of the snake
    def add_segment(self):
        segment = Turtle()
        segment.shape("square")
        # segment.penup()

        segment.color(random.choice(COLORS))
        # to avoid repeating colors
        if len(self.snake) > 0:
            while segment.color() == self.snake[-1].color():
                segment.color(random.choice(COLORS))

        # segment.color("white")
        segment.shapesize(stretch_wid=0.75, stretch_len=0.75)

        # to add segment at the end of the last segment
        if len(self.snake) > 0:
            x_pos = self.snake[-1].xcor()
            segment.setx(x_pos - 15)

        self.snake.append(segment)


    # adds segment to the snake when snake catches the food
    def extend_snake(self):
        self.add_segment()

    def move(self):
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i].setpos(self.snake[i-1].pos())
        self.snake[0].forward(15)

    # set heading of snake on press of arrow keys
    def up(self):
        if self.snake[0].heading() != 270:
            self.snake[0].setheading(90)

    def down(self):
        if self.snake[0].heading() != 90:
            self.snake[0].setheading(270)

    def left(self):
        if self.snake[0].heading() != 0:
            self.snake[0].setheading(180)

    def right(self):
        if self.snake[0].heading() != 180:
            self.snake[0].setheading(0)

    # checks if the head collided with body or tail of the snake
    def check_collision(self):
        # slice of snake excluding head
        snake_body = self.snake[1:]
        for segment in snake_body:
            if self.head.distance(segment) < 10:
                return True

        return False

    def reset_snake(self):
        for segment in self.snake:
            segment.hideturtle()
        self.snake = []
        self.create_snake()
        self.head = self.snake[0]