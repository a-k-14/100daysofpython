import random
word_list = ["aardvark", "baboon", "camel"]

chosen_word = random.choice(word_list)
print(chosen_word)

placeholder = ""
word_length = len(chosen_word)
for position in range(word_length):
    placeholder += "_"
print(placeholder)

is_game_over = False
correct_letters = []
# TODO-1: - Use a while loop to let the user guess again.
while not is_game_over:
    guess = input("Guess a letter: ").lower()

    display = ""
# TODO-2: Change the for loop so that you keep the previous correct letters in display.
    for letter in chosen_word:
        if letter == guess:
            display += letter
            correct_letters.append(letter)
        elif letter in correct_letters:
            display += letter
        else:
            display += "_"

    if "_" not in display:
        is_game_over = True
        print("You win")

    print(display)
