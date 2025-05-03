import my_random

# result = my_random.my_rand_int
result = round(my_random.my_rand_float) + 1

if result == 1:
    print("Heads")
elif result ==2:
    print("Tails")
else:
    print("Sys crashed")