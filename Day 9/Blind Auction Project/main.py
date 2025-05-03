from art import logo
# TODO-1: Ask the user for input
# TODO-2: Save data into dictionary {name: price}
# TODO-3: Whether if new bids need to be added
# TODO-4: Compare bids in dictionary
print(logo)
bids = {}

print("Welcome to the secret auction program.")

to_continue = True

def print_result():
    highest_bid = 0

    for key in bids:
        if bids[key] > highest_bid:
            highest_bid = bids[key]

    for key in bids:
        if bids[key] == highest_bid:
            print(f"The winner is {key} with a bid of ${bids[key]}")

    print(bids[max(bids)])

while to_continue:
    name = input("What is your name?: ")
    bid = int(input("what's your bid?: $"))

    bids[name] = bid

    continue_response = input("Are there any other bidders? Type 'yes' or 'no'. ").lower()

    if continue_response == "no":
        print_result()
        to_continue = False
    else:
        print("\n" * 20)
