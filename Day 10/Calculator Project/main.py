from art import logo

print(logo)

def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return  n1 * n2

def divide(n1, n2):
    return n1 / n2

operations = {
    "+": add,
    '-': subtract,
    '*': multiply,
    '/': divide,
}
use_result = False
result = 0

while True:
    if use_result:
        first_number = result
    else:
        first_number = float(input("what is the first number: "))

    for key in operations:
        print(key)

    choice = input("Pick an operation: ")

    second_number = float(input("What is the next number: "))

    result = operations[choice](first_number, second_number)

    print(f"{first_number} {choice} {second_number} = {result}")

    use_result_choice = input(f"Type 'y' to continue calculating with {result}, or type 'n' to start a new calculation: ").lower()

    if use_result_choice == 'y':
        use_result = True
    else:
        use_result = False
