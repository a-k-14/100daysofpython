import math
import random
import time
from turtle import Screen, Turtle
from player_character import Player, Car

screen = Screen()
screen.setup(width=600, height=500)
screen.bgcolor("old lace")
screen.tracer(0)
screen.listen()

player = Player()
screen.onkey(key="Up", fun=player.move)

number_of_cars = random.randint(2, 8)
prev_y_pos = []
cars = []
for _ in range(0, number_of_cars):

    y_pos = math.ceil(random.uniform(-200, 220))
    while any(y_pos <= i + 25 and y_pos >= i - 25 for i in prev_y_pos):
        y_pos = math.ceil(random.uniform(-220, 220))

    c = Car(y_pos=y_pos)
    cars.append(c)
    prev_y_pos.append(y_pos)

is_game_on = True


screen.update()


while is_game_on:


    screen.update()
    for c in cars:
        if c.xcor() > -300:
            c.move()
            screen.update()
            time.sleep(0.1)

    screen.update()

screen.exitonclick()