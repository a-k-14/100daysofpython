from tkinter import *
from tkinter import messagebox
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
ORIGINAL_DATA = pandas.read_csv("./data/french_words.csv")
WAIT_SECONDS = 5
words_to_learn = []
current_word = {}
no_words_learnt = 0

# ---------------------------- DATA SETUP ------------------------------- #

try:
    words_to_learn_data = pandas.read_csv("./data/words_to_learn.csv")
    words_to_learn = words_to_learn_data.to_dict(orient="records")
    no_words_to_learn = len(words_to_learn)
except FileNotFoundError:
    words_to_learn = ORIGINAL_DATA.to_dict(orient="records")
    no_words_to_learn = len(words_to_learn)
except pandas.errors.EmptyDataError:
    words_to_learn = []
    no_words_to_learn = 0

# if user knows a word, that has to be removed from words_to_learn
def update_words_to_learn():
    global words_to_learn, no_words_learnt

    if len(words_to_learn) > 0:
        words_to_learn.remove(current_word)

        no_words_learnt = no_words_to_learn - len(words_to_learn)
        canvas.itemconfig(card_word_count, text=f"{no_words_learnt}/{no_words_to_learn}")

        words_to_learn_df = pandas.DataFrame(words_to_learn)
        words_to_learn_df.to_csv("./data/words_to_learn.csv", index=False)

        next_card()

# ---------------------------- FUNCTIONALITY SETUP ------------------------------- #
def next_card():

    global flip_timer, current_word

    # cancel the previous window.after() when button is clicked
    window.after_cancel(flip_timer)
    window.after_cancel(timer)

    if len(words_to_learn) > 0:
        current_word = random.choice(words_to_learn)
        word_in_french = current_word["French"]

        canvas.itemconfig(canvas_image, image=card_image_front)
        canvas.itemconfig(card_title, text="French", fill="black")
        canvas.itemconfig(card_word, text=word_in_french, fill="black")

        time_keeper(WAIT_SECONDS)
        flip_timer = window.after(WAIT_SECONDS * 1000, flip_card, current_word["English"])
    else:
        canvas.itemconfig(card_title, text="🏆", fill="black", font=("Arial", 30, "normal"))
        canvas.itemconfig(card_word, text="You have learned all the words!", fill="black", font=("Arial", 25, "bold"))

def flip_card(word_in_english):
    canvas.itemconfig(canvas_image, image=card_image_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=word_in_english, fill="white")

def reset():

    user_confirmation = messagebox.askyesno("Flashy", "Do you want to reset the game and start afresh?")

    if user_confirmation:
        global words_to_learn, no_words_to_learn, no_words_learnt
        words_to_learn = ORIGINAL_DATA.to_dict(orient="records")
        words_to_learn_df = pandas.DataFrame(words_to_learn)
        words_to_learn_df.to_csv("./data/words_to_learn.csv", index=False)
        no_words_to_learn = len(words_to_learn)
        no_words_learnt = 0
        canvas.itemconfig(card_word_count, text=f"{no_words_learnt}/{no_words_to_learn}")
        next_card()

def time_keeper(seconds):
    global timer

    if seconds >= 0:
        canvas.itemconfig(card_timer, text=f"Revealing in: 0{seconds}")
        timer = window.after(1000, time_keeper, seconds - 1)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx=50, pady=20, bg=BACKGROUND_COLOR)
window.title("Flashy")

# when the game launched
# next_card() is called above mainloop()
# this sets off the window.after(...) timer inside the next_card() function
# if user clicks button within 3 sec, the previous window.timer() would still be running and
# now a new window.timer() would be set off
# say, user clicks button 5 times within 3 seconds, then all 5 window.timer() would be set off
# to avoid this, we create the window.timer() as a variable here (for the 1st run)
# and every time the user clicks the button, the previous timer is cancelled with window.after_cancel() and then
# a new window.after() is set off
# this flip timer is not useful, as we cancel it the first time and set it again inside the next_card()
# that is why even though we are not passing any args here, we do not get error
# [TypeError: flip_card() missing 1 required positional argument: 'word_in_english'] -> error we get if we do not pass args
flip_timer = window.after(3000, flip_card)
timer = window.after(1000, time_keeper)


canvas = Canvas(width=600, height=396, bg=BACKGROUND_COLOR, highlightthickness=0)
card_image_front = PhotoImage(file="./images/card_front.png")
card_image_back = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(300, 198, image=card_image_front)
card_title = canvas.create_text(300, 120, text="", font=("Ariel", 35, "italic"))
card_word = canvas.create_text(300, 198, text="", font=("Arial", 50, "bold"))
card_timer = canvas.create_text(460, 340, text="Revealing in: 03", font=("Arial", 16, "italic"))
card_word_count = canvas.create_text(510, 20, text=f"0/{no_words_to_learn}", font=("Arial", 16, "italic"))
canvas.grid(column=0, row=0, columnspan=2)


wrong_button_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_button_image, borderwidth=0, cursor="hand2", highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

right_button_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_button_image, highlightthickness=0, borderwidth=0, cursor="hand2", command=update_words_to_learn)
right_button.grid(column=1, row=1)

reset_button = Button(text="Reset", borderwidth=0, padx=5, pady=2, cursor="hand2", font=("Arial", 12, "normal"), command=reset)
reset_button.grid(column=0, row=2, columnspan=2)


# to show the 1st word
next_card()
window.mainloop()