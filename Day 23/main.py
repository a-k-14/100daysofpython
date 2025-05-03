import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=700, height=500)
screen.bgcolor("old lace")
screen.tracer(0)
screen.listen()

player = Player()
score = Scoreboard()
car_manager = CarManager()

screen.onkeypress(key="Up", fun=player.move)

is_game_on = True
counter = 5
sleep_time = 0.1
while is_game_on:
    time.sleep(sleep_time)
    screen.update()

    # detect collision with any of the cars
    for car in car_manager.all_cars:
        if player.distance(car) < 20:
            is_game_on = False
            score.game_over()

    # player has crossed successfully and goes to next level
    if player.ycor() >= 250:
        score.update_level()
        player.reset_pos()
        # car_manager.reset_cars()
        sleep_time *= 0.5

    # generate new car on every 6th run of the loop
    if counter % 5 == 0:
        car_manager.create_car()

    # to track the loop runs
    counter += 1
    car_manager.move_cars()


screen.exitonclick()