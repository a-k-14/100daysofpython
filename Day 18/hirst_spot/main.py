import random
import turtle as t
import colorgram

def get_color():
    # extract 10 colors from the image
    colors = colorgram.extract("source.jpg", 30)

    return colors

def main():
    # create Turtle object
    toise = t.Turtle()

    # get image colors
    image_colors = get_color()

    t.colormode(255)
    toise.speed("fastest")
    toise.hideturtle()
    toise.penup()
    toise.setposition(-300, -200)

    # to print 10 x 10 matrix of dots
    n = 1
    while n <= 10:
        for _ in range(10):
            random_color = random.choice(image_colors)
            toise.dot(20, random_color.rgb)
            toise.forward(50)

        toise.setx(-300)
        toise.sety(toise.ycor() + 50)
        n += 1

    my_screen = t.Screen()
    my_screen.exitonclick()

# get_color()
main()