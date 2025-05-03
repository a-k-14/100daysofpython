import turtle as t
import pandas as pd

# 1. setup turtle screen with bg image
# 2. get the 50_states data from csv into a dict, get the number of states
# 3. get user input of state name, convert to lower case - repeat till 50 states are guessed
# 4. if the user input matches with any state, get the state coordinates
# track the number of states correctly guessed
# 5. show the state name in the screen at that coordinates

# screen setup
screen = t.Screen()
# screen.setup(width=725, height=491)
screen.bgpic("blank_states_img.gif")
screen.title("Guess the US States")

# data setup
df = pd.read_csv("50_states.csv")
# for use in list comprehension
states = df.state.to_list()
num_of_states = len(states)
# x_coordinates = df.x.to_list()
# y_coordinates = df.y.to_list()
# print(states)

# num_of_states = len(df.state)
correct_guesses = 0
# for use in list comprehension
guessed_states = []

# turtle setup to write the state name on the screen
turtle = t.Turtle()
turtle.penup()
turtle.hideturtle()

while correct_guesses < 51:
    user_input = screen.textinput(title=f"{correct_guesses}/{num_of_states} states correct",
                                  prompt="What's another state name?              ").title()
    # for state in states:
    #     if state.lower() == user_input:
    #         state_index = states.index(state)
    #         x_pos = x_coordinates[state_index]
    #         y_pos = y_coordinates[state_index]
    #
    #         turtle.goto(x=x_pos, y=y_pos)
    #         turtle.write(states[state_index])
    #
    #         correct_guesses += 1

    # get the matching row with user_input if exists

    # exit the loop on exit input
    if user_input == "Exit":
        # write the missed states to a list
        # missed_states = {"missed state": []}
        # for state in states:
        #     if state not in guessed_states:
        #         missed_states["missed state"].append(state)

        # using list comprehension
        missed_states = [state for state in states if state not in guessed_states]

        missed_states_df = pd.DataFrame(missed_states)
        missed_states_df.to_csv("Missed States.csv")
        break

    # we can also check in 'if in states' if the following is resource intensive
    match = df[df.state == user_input]
    # print(match)
    if not match.empty:
        guessed_states.append(user_input)
        x_pos = match.x.item()
        y_pos = match.y.tolist()[0]
        state = match.state.tolist()[0]

        turtle.goto(x=x_pos, y=y_pos)
        turtle.write(state)

        correct_guesses += 1



# with open("test.csv", mode="w") as file:
#     file.write(missed_states)

# to check the positions of state names on the image
# for state in states:
#     index = states.index(state)
#     x = x_coordinates[index]
#     y = y_coordinates[index]
#     turtle.setpos(x=x, y=y)
#     turtle.write(state)
#
# print("Done")

# screen.exitonclick()