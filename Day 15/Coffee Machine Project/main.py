MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}


def check_resources(resources_available, ingredients):
    """
    Checks if there are sufficient resources available for the user's choice and returns a boolean
    :param resources_available:
    :param ingredients:
    :return: True - if available, False - if not available
    """
    # ingredients = MENU[user_choice]["ingredients"]

    for ingredient in ingredients:
        if resources_available[ingredient] < ingredients[ingredient]:
                print(f"Sorry there is not enough {ingredient}.")
                return False

    return True

def user_input_coins(denomination):
    """
    Gets the coins from the user for a respective denomination and returns the same
    :param denomination:
    :return: coins in float
    """
    while True:
        try:
            user_input = float(input(f"How many {denomination}?: "))
            break
        except ValueError:
            print("Wrong input")


    return user_input


def get_total_money_received():
    """
    :return: $ equivalent of total of coins received
    """
    print("please insert coins.")

    coin_denomination = {
        "quarters": user_input_coins("quarters") * 0.25,
        "dimes": user_input_coins("dimes") * 0.10,
        "nickles": user_input_coins("nickles") * 0.05,
        "pennies": user_input_coins("pennies") * 0.01
    }

    return sum(coin_denomination.values())


def main():
    resources = {
        "water": 300,
        "milk": 200,
        "coffee": 100,
    }

    # total sales
    money = 0

    # run the machine till 'off' is entered as input for choice
    while True:

        # validate user input to avoid KeyError in check_resources() function
        while True:
            choice = input("What would you like? (espresso/latte/cappuccino): ").lower()
            if choice in MENU or choice in ["report", "off"]:
                break
            else:
                print("Wrong option selected!")

        if choice == "off":
            return
        # print the inventory
        elif choice == "report":
            for resource in resources:
                print(f"{resource.capitalize()}: {resources[resource]}{'g' if resource == 'coffee' else 'ml'}")
            print(f"Money: ${money}")
            continue
        else:
            choice_ingredients = MENU[choice]["ingredients"]
            if not check_resources(resources, choice_ingredients):
                return

        # get coins from the user and calculate the $ equivalent of the total coins
        total_money_received = get_total_money_received()
        choice_cost = MENU[choice]["cost"]

        if total_money_received > choice_cost:
            money += choice_cost
            refund = round(total_money_received - choice_cost, 2)
            print(f"Here is ${refund} dollars in change.")
        elif total_money_received < choice_cost:
            print(f"Sorry {total_money_received} not enough for {choice} which is {choice_cost}. Money refunded.")
            return

        # Update the resources to reflect the quantity consumed for the user's choice
        for ingredient in choice_ingredients:
            resources[ingredient] = resources[ingredient] - choice_ingredients[ingredient]

        print(f"Here is your {choice}. Enjoy!")

main()