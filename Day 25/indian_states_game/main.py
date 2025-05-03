import turtle
import pandas

# Show a input box for user to input the state - turtle
# if the state is correct, show the state in the map - turtle
# and prompt for the next state - turtle
# states data is in csv - covert to df - list

# screen setup
screen = turtle.Screen()
# screen.setup(width=740, height=760)
screen.bgpic("bg_pic.gif")

# data setup
# get the data from csv to df
df = pandas.read_csv("states.csv")
# print(df)
# print(df.x.max())
# print(df.x.min())
# print(df.y.max())
# print(df.y.min())

# get the states as a list
states = df.state.to_list()
# print(states)

# track the correctly guessed states to show length in input box title and also to create the missing states list
correct_states = []

my_turtle = turtle.Turtle()
my_turtle.hideturtle()

while len(correct_states) < len(states):
    user_input = screen.textinput(title=f"Got {len(correct_states)}/{len(states)} states.", prompt="Enter the state name                            ").title()

    # to handle and
    user_input = user_input.replace(" And ", " and ")

    if user_input == "Exit":
        # generate a csv of missing states
        missing_states = [state for state in states if state not in correct_states]
        df_missing_states = pandas.DataFrame(missing_states, columns=["state"])
        df_missing_states.to_csv("missing_states.csv")
        break

    if user_input in states:
        correct_states.append(user_input)
        df_row = df[df.state == user_input]
        x_cor = int(df_row.x.to_list()[0])
        y_cor = int(df_row.y.to_list()[0])

        my_turtle.goto(x=x_cor, y=y_cor)
        my_turtle.write(arg=user_input)



screen.exitonclick()