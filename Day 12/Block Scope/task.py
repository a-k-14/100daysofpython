import math

def is_prime(n):
    if n < 2:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False

    # we add 1 to sqrt as range counts from 3 to sqrt, excl. sqrt
    for i in range(3, math.ceil(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            print(i)
            return False

    return True

while True:
    num = int(input("Enter a number to check if prime: "))
    print(is_prime(num))