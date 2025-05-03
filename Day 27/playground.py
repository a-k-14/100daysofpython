def func(a=1, b=4, c=9):
    print(a, b, c)

# func(10, 8, 12)
# func(b=7)

def new_func(*args):
    print(type(args))
    # for n in args:
    #     print(n)
    return sum(args)

# print(new_func(-1, 3, 4, 1, 4))

def another_func(**kw):
    print(type(kw))
    print(kw)
    print(kw.get("add"))
    print(kw["divide"])
    print(kw.get("modulo"))

# another_func(add=2, multiply=3, divide=5)

class Car:
    def __init__(self, tyres=4, **kw):
        # may throw an error if 'make' not specified, so use .get()
        self.make = kw["make"]
        self.model = kw.get("model")
        self.color = kw.get("color")
        self.tyres = tyres
        print(kw)


my_car = Car(make="BMW", tyres=5, model="M2")
print(my_car.make)
print(my_car.model)
print(my_car.tyres)
