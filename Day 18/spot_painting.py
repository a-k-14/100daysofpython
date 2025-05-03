import turtle as t
import random

import colorgram

def draw_spot_painting():
    colors = ["royal blue", "tan", "gold", "sienna", "crimson", "rosy brown", "dark orchid", "slate blue",
              "light sea green", "olive drab", "blanched almond"]
    toise = t.Turtle()

    toise.speed("fastest")

    toise.penup()
    toise.setposition(-300, -200)
    toise.pendown()

    n = 1

    while n <= 10:
        for _ in range(10):
            toise.color(random.choice(colors))
            toise.begin_fill()
            toise.circle(10)
            toise.end_fill()
            toise.penup()
            toise.forward(50)
            toise.pendown()
        n += 1
        toise.penup()
        toise.setx(-300)
        toise.sety(toise.ycor() + 50)
        toise.pendown()

draw_spot_painting()