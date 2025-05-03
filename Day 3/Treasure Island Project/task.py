print(r'''
*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\ ` . "-._ /_______________|_______
|                   | |o ;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/_____ /
*******************************************************************************
''')
print("Welcome to Treasure Island.")
print("Your mission is to find the treasure.")

left_right = input("You are in the middle of a forest🐞😨, do you want to go LEFT or RIGHT? ")

if left_right.lower() != "left":
    print("You fell in to a hole🕳. Game over😱")

to_swim = input("Well done. You have to cross the lake. Do you want to SWIM🏊‍♀️ or WAIT for the boat🚢? ")

if to_swim.lower() != "wait":
    print("Slow and steady wins the race😠. Attacked by trout😭. Game over😨")

which_door = input("Patience pays👏. There's are RED, YELLOW, and BLUE doors🚪. Which one you want to go through🧟‍?  ️")

if which_door.lower() == "red":
    print("Burned by fire🔥. Game over😨")
elif which_door.lower() == "yellow":
    print("Hurray! You win🏆🤴")
elif which_door.lower() == "blue":
    print("Eaten by beasts🍜. Game over😨")
else:
    print("Game over🙏")