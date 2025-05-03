from turtle import Turtle, Screen

toi = Turtle()
scr = Screen()

def move_forward():
    toi.forward(5)

def move_backward():
    toi.backward(5)

def up():
    toi.setheading(90)

def down():
    toi.setheading(270)

def left():
    toi.setheading(180)

def right():
    toi.setheading(0)

def clockwise():
    toi.right(5)

def counter_clockwise():
    toi.left(5)

def clear_screen():
    toi.setposition(0, 0)
    toi.clear()

scr.listen()
scr.onkey(key="space", fun=move_forward)
scr.onkey(key="w", fun=move_forward)
scr.onkey(key="s", fun=move_backward)
scr.onkey(key="a", fun=clockwise)
scr.onkey(key="d", fun=counter_clockwise)
scr.onkey(key="Up", fun=up)
scr.onkey(key="Down", fun=down)
scr.onkey(key="Left", fun=left)
scr.onkey(key="Right", fun=right)
scr.onkey(key="c", fun=clear_screen)

scr.exitonclick()
