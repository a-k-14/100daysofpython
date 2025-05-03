import random
"""
Goal: To pick a user on a randon basis from a list of users
Algorithm:
1. make a list of users
2. setup random number generator to generate numbers from 0 to list length-1
3. get the user at the index randomly generated
"""

friends = ["Alice", "Bob", "Charlie", "David", "Emanuel"]
list_length = len(friends)

random_index = random.randint(0, list_length - 1)

print(f"The lucky friend is: {friends[random_index]}")
print(f"The lucky friend is: {random.choice(friends)}")
