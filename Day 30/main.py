# FileNotFoundError
try:
    print("Try")
    file = open("data.txt")
except FileNotFoundError as error_message:
    print("Except")
    print(error_message)
    file = open("data.txt", "a")
    file.write("A line1\n")
else:
    print("Else")
    file = open("data.txt", "a")
    file.write("A line2\n")
    # print(file.read())
finally:
    print("Finally")
    file = open("data.txt")
    print(file.read())
    file.close()
    # raise FileNotFoundError("This is a made up error")

# custom error messages

# BMI calculator
height = float(input("Enter your height in meters: "))
weight = float(input("Enter your weight in kilograms: "))

if height > 3:
    raise ValueError("Human height cannot be more than 3 meters")

print(f"BMI: {round(weight / height**2)}")