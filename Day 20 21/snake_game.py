import turtle
import time
from snake import Snake
from food import Food
from scoreboard import Scoreboard

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
# 500 / 2 = 250 with a margin of 10 = 240
EDGE = SCREEN_WIDTH / 2 - 10

screen = turtle.Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.title("Classic Snake Game")
screen.bgcolor("black")
screen.tracer(n=0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(key="Up", fun=snake.up)
screen.onkey(key="Down", fun=snake.down)
screen.onkey(key="Left", fun=snake.left)
screen.onkey(key="Right", fun=snake.right)

is_game_on = True
while is_game_on:

    time.sleep(0.1)
    screen.update()

    # detect collision with food
    if snake.head.distance(food) <= 15:
        food.refresh()
        scoreboard.update_score()
        snake.extend_snake()

    # detect collision with walls
    if snake.head.xcor() > EDGE or snake.head.xcor() < -EDGE or snake.head.ycor() > EDGE or snake.head.ycor() < -EDGE:
        is_game_on = False
        scoreboard.write_game_over()

    # detect collision with tail
    # if head collied with any part of the snake, it is game over
    if snake.check_collision():
        is_game_on = False
        scoreboard.write_game_over()

    snake.move()

screen.exitonclick()