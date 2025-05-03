x = 10  # Global variable

def modify_global():
    x = 20  # This creates a new local variable x, not modifying the global x
    if x < 12:
        print("ok")
    print("Inside function:", x)

modify_global()  # Output: Inside function: 20
print("Outside function:", x)  # Output: Outside function: 10 (global x is unchanged)