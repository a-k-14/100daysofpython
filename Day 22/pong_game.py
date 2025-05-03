from turtle import Turtle, Screen
from paddle import Paddle
from scoreboard import Scoreboard
import ball
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

# set the screen
screen = Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.bgcolor("black")
screen.title("Pong")
screen.tracer(0)

# screen separator
# separator_segments = []
y_pos = SCREEN_HEIGHT / 2 - 40
for i in range(0, 15):
    t = Turtle(shape="square")
    t.color("white")
    t.shapesize(stretch_len=0.25, stretch_wid=0.75)
    t.penup()
    t.sety(y_pos)
    # separator_segments.append(t)
    y_pos -= 30


r_paddle = Paddle(position=(350, 0))
l_paddle = Paddle(position=(-350, 0))
ball = ball.Ball()
r_score = Scoreboard(position=(100, 180))
l_score = Scoreboard(position=(-100, 180))

screen.listen()
screen.onkeypress(key="Up", fun=r_paddle.up)
screen.onkeypress(key="Down", fun=r_paddle.down)

screen.onkeypress(key="w", fun=l_paddle.up)
screen.onkeypress(key="d", fun=l_paddle.down)


is_game_on = True
while is_game_on:
    screen.update()
    ball.move()
    time.sleep(0.1)

    # detect collision with top or bottom edge
    if ball.ycor() > 230 or ball.ycor() < -230:
        ball.bounce_y()

    # detect collision with paddles
    if r_paddle.distance(ball) < 50 and ball.xcor() > 320:
        ball.bounce_x()
        r_score.update_score()
    # detect if r_paddle missed the ball
    elif ball.xcor() > 400:
        ball.reset_pos()
        l_score.update_score()

    if l_paddle.distance(ball) < 50 and ball.xcor() < -320:
        ball.bounce_x()
        l_score.update_score()
    # detect if l_paddle missed the ball
    elif ball.xcor() < -400:
        ball.reset_pos()
        r_score.update_score()

screen.exitonclick()