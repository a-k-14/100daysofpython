import pandas as pd
import turtle as t


# to generate the NATO phonetic for user input word

# make DF from csv data
df = pd.read_csv("nato_phonetic_alphabet.csv")
# print(df.letter.to_list())

# create a dict from df "A":"Alpha", using dictionary comprehension
phonetic_dict = {row.letter:row.code for (index, row) in df.iterrows()}
# print(phonetic_dict)

# looks like this method creates a stack of function calls when number is entered and stack unwinds only at th end when word is entered
def generate_phonetic():
    user_input = input("Enter the word: ").upper()

    try:
        phonetic_list = [phonetic_dict[letter] for letter in user_input]
    except KeyError:
        print("Sorry, only alphabets in the word please.")
        generate_phonetic()
    else:
        print(phonetic_list)


generate_phonetic()
