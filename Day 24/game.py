from turtle import Screen
from scoreboard import Scoreboard
from food import Food
import snake
import time

# setup screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
X_EDGE = SCREEN_WIDTH / 2 - 10
Y_EDGE = SCREEN_HEIGHT / 2 - 10

screen = Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.bgcolor("black")
screen.title("The Classic Snake Game")
# screen.tracer(0)

scoreboard = Scoreboard(screen_height=SCREEN_HEIGHT)
food = Food(screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
snake = snake.Snake()

screen.listen()
screen.onkey(key="Up", fun=snake.up)
screen.onkey(key="Down", fun=snake.down)
screen.onkey(key="Left", fun=snake.left)
screen.onkey(key="Right", fun=snake.right)

is_game_on = True
while is_game_on:
    time.sleep(0.1)
    screen.update()

    # check snake collision with itself
    if snake.check_collision():
        # scoreboard.game_over()
        # is_game_on = False
        scoreboard.reset_score()
        time.sleep(0.5)
        snake.reset_snake()

    # detect collision with walls
    if snake.head.xcor() >= X_EDGE or snake.head.xcor() <= -X_EDGE or snake.head.ycor() >= Y_EDGE or snake.head.ycor() <= -Y_EDGE:
        # scoreboard.game_over()
        # is_game_on = False
        scoreboard.reset_score()
        time.sleep(0.5)
        snake.reset_snake()

    # detects collision with food
    if snake.head.distance(food) < 15:
        snake.add_segment()
        scoreboard.update_score()
        food.move()

    snake.move()

screen.exitonclick()