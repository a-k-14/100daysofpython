import random
import turtle as t

my_turtle = t.Turtle()

# draw a dashed line
# for _ in range(4):
#     for _ in range(10):
#         my_turtle.forward(10)
#         my_turtle.penup()
#         my_turtle.forward(10)
#         my_turtle.pendown()
#     my_turtle.left(90)

# draw a pentagon whose side are at an angle of 72deg
# for _ in range(3):
#     my_turtle.forward(100)
#     my_turtle.left(360 / 3)

# function to change the turtle color
def change_color():
    t.colormode(255)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    my_turtle.color((r, g, b))

def draw_ten_shapes():
    # start with 3 sides
    n = 3

    # move the turtle up so that all shapes are visible on the screen
    my_turtle.penup()
    my_turtle.setx(-100)
    my_turtle.sety(300)
    my_turtle.pendown()

    while n <= 10:
        change_color()
        for _ in range(n):
            my_turtle.forward(50)
            my_turtle.right(360 / n)
        n += 1
        print(n)


def draw_random_walk():
    colors = ["royal blue", "tan", "gold", "sienna", "crimson", "rosy brown", "dark orchid", "slate blue",
              "light sea green", "olive drab", "blanched almond"]
    # set thickness of line
    my_turtle.width(8)
    directions = [0, 90, 180, 270]

    my_turtle.speed("fastest")

    for _ in range(200):
        # my_turtle.color(random.choice(colors))
        change_color()
        my_turtle.forward(30)
        my_turtle.setheading(random.choice(directions))


def draw_circle():
    my_turtle.speed("fastest")
    deg_to_turn = 5
    times_to_repeat = int( 360 / deg_to_turn )

    for _ in range(times_to_repeat):
        change_color()
        my_turtle.circle(100)
        # my_turtle.left(deg_to_turn)
        # my_turtle.tilt(5)
        my_turtle.setheading(my_turtle.heading() + deg_to_turn)



# draw_random_walk()
draw_circle()



my_screen = t.Screen()
my_screen.exitonclick()
