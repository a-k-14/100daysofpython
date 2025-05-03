# from turtle import Turtle, Screen
from prettytable import PrettyTable
#
# timmy = Turtle()
# print(timmy)
# timmy.color("black", "VioletRed")
# timmy.shape("turtle")
# timmy.forward(80)
# timmy.left(150)
# timmy.forward(90)
# timmy.home()
#
# for steps in range(5):
#     for c in ('blue', 'red', 'green'):
#         timmy.color(c)
#         timmy.forward(steps)
#         timmy.right(30)

# # timmy.home()

# my_screen = Screen()
# # print(my_screen.canvheight)
# # print(my_screen.canvwidth)
# my_screen.exitonclick()

pokedox = {
    "Pikachu ": 125,
    "Startle ": 280,
    "Geodude ": 175 ,
    "Ampharos": 181,
}

# print("+------------------+-------+")
# print("|  Pokemon Name    | Score |")
# print("+------------------+-------+")
#
# for pokemon in pokedox:
#     print(f"|  {pokemon}        | {pokedox[pokemon]}   |")
#
# print("+------------------+-------+")

# create table using prettytable package
table = PrettyTable()

# get the keys from pokedox as a list using list()
table.add_column("Pokemon Name", list(pokedox.keys()))
table.add_column("Score", list(pokedox.values()))

print(table)
# sort table by score in descending
print(table.get_string(sortby="Score", reversesort = True))

# left align the table and sort by name
table.align["Pokemon Name"] = "l"
# print(table.align)
print(table.get_string(sortby="Pokemon Name"))
