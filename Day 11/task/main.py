from art import logo
import random

# continue_game = True
# start_game = input("Do you want to play a game of Blackjack🃏? Type 'y' or 'n': ").lower()
#
# if start_game == "n":
#     continue_game = False

# to add cards to the user or computer
def cards_dealer():
    """Randomly appends a card from the deck to the list provided for num_of_card times"""
    deck = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(deck)

# adjust for ace as 11 or 1
def adjust_for_ace(cards):
    """If score > 21, replaces the 11 with 1"""
    while sum(cards) > 21 and 11 in cards:
        # index_of_ace = cards.index(11)
        # cards[index_of_ace] = 1
        cards.remove(11)
        cards.append(1)

def print_result(user_final_score, computer_final_score):
    if user_final_score > 21:
        print("You went over. You lose 🙄")
    # user_cards_sum > 21 mau be true at the 1st run itself or after while loop
    elif computer_final_score > 21:
        print("Opponent went over. You win 😎")
    elif user_final_score == 21:
        print("Lose, opponent has Blackjack🙄")
    elif user_final_score == 21:
        print("Win with a Blackjack😎")
    elif user_final_score == computer_final_score:
        print("Draw 🤗")
    # both user_cards_sum and computer_cards_sum are < 21 or == 21
    elif user_final_score > computer_final_score:
        print("User wins")
    elif computer_final_score > user_final_score:
        print("Computer wins")

def play_game():

    user_cards = []
    computer_cards = []

    # deal 2 cards at the start
    for _ in range(2):
        user_cards.append(cards_dealer())
        computer_cards.append(cards_dealer())

    adjust_for_ace(user_cards)
    user_score = sum(user_cards)

    adjust_for_ace(computer_cards)
    computer_score = sum(computer_cards)

    print(f"    Your cards: {user_cards}, current score: {user_score}")
    # only show the 1st card of the computer
    print(f"    Computer's first card: {computer_cards[0]}")

    # let user draw cards or pass while total of user_cards_sum < 21
    while user_score < 21:
        draw_or_pass = input("Type 'y' to get another card, type 'n' to pass: ").lower()
        if draw_or_pass == "y":
            user_cards.append(cards_dealer())
            adjust_for_ace(user_cards)
            user_score = sum(user_cards)
            print(f"    Your cards: {user_cards}, current score: {user_score}")
            print(f"    Computer's first card: {computer_cards[0]}")
        elif draw_or_pass == "n":
            break

    # we have user_cards_sum condition check here so that we can have one set of print statements
    # for user_cards_sum > 21 and <= 21 as well
    while user_score <= 21 and computer_score <= 16:
        computer_cards.append(cards_dealer())
        adjust_for_ace(computer_cards)
        computer_score = sum(computer_cards)

    print("*************************************************************")
    print(f"    Your final hand: {user_cards}, final score: {user_score}")
    print(f"    Computer's final hand: {computer_cards}, final score: {computer_score}")

    print_result(user_score, computer_score)


# loop to keep the game running while users response to continue_game_response is y
while input("\nDo you want to play a game of Blackjack🃏? Type 'y' or 'n': ").lower() == "y":
    # print the new lines at the start to hide the 1st question
    print("\n" * 15)

    print(logo)

    play_game()

    # continue_game_response = input("\nDo you want to play a game of Blackjack🃏? Type 'y' or 'n': ").lower()
    # if continue_game_response == "n":
    #     continue_game = False
    # elif continue_game_response == "y":
    #     continue_game = True
