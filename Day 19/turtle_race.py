import random
from turtle import Turtle, Screen

colors = ["violet", "indigo", "blue", "green", "gold", "orange", "red"]

screen = Screen()
screen.setup(width=600, height=500)
user_guess = screen.textinput("Welcome to the turtle race!", "Which color turtle is going to win?")

turtles = []
# to space the turtles next to each other with a gap of 30 (-90 to +90)
y_pos = -90

for c in colors:
    t = Turtle(shape="turtle")
    # t.shape("turtle")
    t.speed("slow")
    t.penup()
    t.color(c)
    # t.setpos(x=-300 + 20, y=y_pos)
    # t.goto(x=-300 + 20, y=y_pos)
    turtles.append(t)
    # y_pos += 30

for t in turtles:
    t.goto(x=-300 + 20, y=y_pos)
    y_pos += 30

continue_race = False
winner_color = "none"

if user_guess:
    continue_race = True

while continue_race:
    for t in turtles:
        movement = random.randint(1, 5)
        # if any of the turtles reached the edge, end the game
        # we use >= 300 - 20 instead of =, as adding the movement might make the turtle cross 300 - 20
        # if turtle xcor() is 279, then adding movement of 3 will take it to 282, which is beyond 300 - 20
        if t.xcor() + movement >= 300 - 20:
            t.forward(300 - 20 - t.xcor())
            winner_color = t.fillcolor()
            if user_guess == winner_color:
                print(f"The {winner_color} turtle won the race and you win.")
            else:
                print(f"You lose. The {winner_color} turtle is the winner. You chose {user_guess} turtle")
            continue_race = False
            break
        else:
            t.forward(movement)



screen.exitonclick()
