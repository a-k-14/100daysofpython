from turtle import Turtle

FONT = ("Courier", 12, "normal")

class Scoreboard(Turtle):
    def __init__(self, screen_height):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("white")
        self.score = 0
        # 1. open the file
        # 2. read the contents
        # 3. convert the contents (we get string) to int
        with open("data.txt") as data:
            self.high_score = int(data.read())
        self.goto(0, screen_height / 2 - 40)
        self.write_score()

    def write_score(self):
        self.clear()
        self.write(arg=f"Score: {self.score}. High Score: {self.high_score}", align="center", font=FONT)

    def update_score(self):
        self.score += 1
        self.write_score()

    def game_over(self):
        self.goto(0, 0)
        self.write(arg="Game Over", align="center", font=FONT)

    def reset_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            # 1. open the file
            # 2. convert the self.high_score to string, as write only takes strings
            # 3. write the self.high_score to the file
            with open("data.txt", mode="w") as data:
                data.write(f"{self.high_score}")
        self.score = 0
        self.write_score()