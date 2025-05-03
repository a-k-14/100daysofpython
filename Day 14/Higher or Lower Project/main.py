import random
from art import logo, vs
from game_data import data

# to format the dictionary into a choice
def format_data(data_point):
    return data_point["name"] + ", a " + data_point["description"] + ", from " + data_point["country"] + "."

def play_round(data_point_1, data_point_2):

    follower_count_1 = data_point_1["follower_count"]
    follower_count_2 = data_point_2["follower_count"]

    print(f"Compare A: {format_data(data_point_1)} {follower_count_1}")
    print(vs)
    print(f"Against B: {format_data(data_point_2)} {follower_count_2}")

    user_guess = input("Who has more followers? Type 'A' or 'B': ").lower()
    # data_point_1 = data_point_2

    # return if the game is over
    if user_guess == 'a' and follower_count_1 > follower_count_2:
        return False
    elif user_guess == 'b' and follower_count_2 > follower_count_1:
        return False
    else:
        return True

    # if follower_count_1 > follower_count_2:
    #     return user_guess == 'a'
    # else:
    #     return user_guess == 'b'

def main():

    print("\n" * 20)
    print(logo)

    # game over when user answers wrong
    is_game_over = False
    user_score = 0
    # declared option_1_data point here to ensure option_1 would be option_2 from 2nd round
    option_1_data = random.choice(data)

    while not is_game_over:

        option_2_data = random.choice(data)

        while option_2_data == option_1_data:
            option_2_data = random.choice(data)

        is_game_over = play_round(option_1_data, option_2_data)

        print("\n" * 20)
        print(logo)

        if not is_game_over:
            option_1_data = option_2_data
            user_score += 1
            print(f"You're right! Current score: {user_score}.")
        else:
            print(f"Sorry, that's wrong. Final score: {user_score}")

main()