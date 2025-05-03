from turtle import Turtle

ALIGNMENT = "center"
FONT = ('Courier', 12, 'bold')

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("white")
        self.hideturtle()
        # place the score at the top center of the screen
        self.setpos(x= 0, y=225)
        self.write_score()

    def write_score(self):
        self.clear()
        self.write(arg=f"Score: {self.score}", align=ALIGNMENT, font=FONT)

    def update_score(self):
        self.score += 1
        self.write_score()

    def write_game_over(self):
        self.goto(x=0, y=0)
        self.write(arg="GAME OVER", align=ALIGNMENT, font=FONT)