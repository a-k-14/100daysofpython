import pandas as pd
import turtle as t


# to generate the NATO phonetic for user input word

# make DF from csv data
df = pd.read_csv("nato_phonetic_alphabet.csv")
# print(df.letter.to_list())

# create a dict from df "A":"Alpha", using dictionary comprehension
phonetic_dict = {row.letter:row.code for (index, row) in df.iterrows()}
# print(phonetic_dict)

# user_input = input("Enter the word: ").upper()
# phonetic_list = [phonetic_dict[letter] for letter in user_input]

# for letter in user_input:
#     phonetic_word = phonetic_dict[letter.upper()]
#     phonetic_list.append(phonetic_word)

# print(phonetic_list)

screen = t.Screen()
screen.title("Get the NATO phonetic for your word")
screen.bgcolor("black")

my_turtle = t.Turtle()
my_turtle.hideturtle()
my_turtle.color("white")

user_input = screen.textinput("NATO phonetic", "Enter the word                             ")

phonetic_list = [phonetic_dict[letter] for letter in user_input.upper()]
# how to wrap text?
my_turtle.write(arg=f"NATO phonetic for {user_input}: \n\n{phonetic_list}", align="center", font=("Courier", 8, "bold"))

screen.exitonclick()