from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10
EDGE = int(500 / 2 - 60)

class CarManager:
    def __init__(self):
        self.all_cars=[]

    def create_car(self):
        car = Turtle(shape="square")
        car.penup()
        car.shapesize(stretch_len=2)
        car.color(random.choice(COLORS))

        y_pos = random.randint(-EDGE, EDGE)
        # ensures cars do not overlap

        # check if the cars list is not empty
        if len(self.all_cars) != 0:
            # check if the new car y_pos is within +/- 25px of last car y_pos
            while y_pos <= self.all_cars[-1].ycor() + 25 and y_pos >= self.all_cars[-1].ycor() - 25:
                y_pos = random.randint(-200, 200)

        car.goto(350, y_pos)
        self.all_cars.append(car)

    def move_cars(self):
        # to add cars that have not reached the left edge so that we need to check all cars everytime
        updated_cars = []

        for car in self.all_cars:
            if car.xcor() >= -400:
                car.setx(car.xcor() - STARTING_MOVE_DISTANCE)
                updated_cars.append(car)

        self.all_cars = updated_cars

    # reset cars list on new level
    def reset_cars(self):
        for car in self.all_cars:
            car.hideturtle()
        self.all_cars = []