from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

# create menu items
# espresso = MenuItem(name = "espresso", cost = 1.5, water = 50, milk = 0, coffee = 18)
# latte = MenuItem(name = "latte", cost = 2.25, water = 200, milk = 150, coffee = 24)
# capuccino = MenuItem(name = "capuccino", cost = 3.0, water = 250, milk = 100, coffee = 24)

# create the menu card
shop_menu = Menu()

# add menu items to the menu card
# shop_menu.menu = [espresso, latte, capuccino]

# coffee maker
coffe_machine = CoffeeMaker()
print(coffe_machine)

# bill processor
cash_register = MoneyMachine()

machine_is_on = True

while machine_is_on:
    # get the order from the user
    user_response = input(f"What do you want to order - {shop_menu.get_items()}: ").lower()

    if user_response == "off":
        machine_is_on = False
    elif user_response == "report":
        coffe_machine.report()
        cash_register.report()
    else:
        order = shop_menu.find_drink(user_response)

        # check the resource availability
        res_available = coffe_machine.is_resource_sufficient(order)

        # collect and process payment if res are available
        if res_available and cash_register.make_payment(order.cost):
            # if sufficient money received then serve the order
            # print(shop_menu.menu[0].name)
            coffe_machine.make_coffee(order)