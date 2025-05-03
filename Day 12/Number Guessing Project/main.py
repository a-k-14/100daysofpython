"""
1. print welcome
2. get a random number 1 - 100
3. get diff choice from user
4. set no of rounds
5. loop - while rounds > 0
get a guess
if it matches random num - win
else
guess > rand - too high
guess < rand - too low
rounds --
"""
import random
from art import logo

EASY_LEVEL_TURNS = 10
HARD_LEVEL_TURNS = 5

# in this game, the attempt variable was declared in while loop, but can be used in the play_game function as well
def play_game(attempts, number_to_guess):
    # global attempts
    while attempts > 0:
        print(f"You have {attempts} attempts remaining to guess the number.")

        user_guess = int(input("Make a guess: "))

        if user_guess == number_to_guess:
            print(f"You got it! The answer was {number_to_guess}.")
            break

        if user_guess < number_to_guess:
            print("Too low")
        elif user_guess > number_to_guess:
            print("Too high")

        attempts -= 1

        if attempts == 0:
            print("You've run out of guesses. Refresh the page to run again.")
        else:
            print("Guess again.")

while input("Do you want to play a game ('y' or 'n'): ").lower() == 'y':

    print("\n" * 20)
    print(logo)

    print("Welcome to the Number Guessing Game!")
    print("I'm of thinking of a number between 1 and 100")

    random_num = random.randint(1, 100)

    difficulty_level = input("Choose difficulty: type 'easy' or 'hard' -> ").lower()

    if difficulty_level == "easy":
        user_attempts = EASY_LEVEL_TURNS
    else:
        user_attempts = HARD_LEVEL_TURNS

    play_game(user_attempts, random_num)