# get user input and convert to int

test = 5 / 2

print(test)

num = int(input("Enter the number to check odd/even: "))

if num % 2 == 0:
    print(f"{num} is 'even'")
else:
    print(f"{num} is 'odd'")