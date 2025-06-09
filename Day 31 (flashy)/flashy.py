from tkinter import *
from tkinter import messagebox
import pandas
import random
from tkinter import ttk

from pandas.core.interchange.dataframe_protocol import DataFrame

BACKGROUND_COLOR = "#B1DDC6"
ORIGINAL_DATA = pandas.read_csv("./data/french_words.csv")
words_to_learn = []
known_words = []
# we create this outside so that this can be used in the flip_card function inside the 1st window.after()
current_word = {}
WAIT_SECONDS = 3
# to enable cancellation of time_keeper() when button is clicked
timer = None

# ---------------------------- DATA SETUP ------------------------------- #

# check if words_to_learn.csv exists
# if it exists, words_to_learn = words_to_learn.csv
# else words_to_learn = original_data
try:
    words_to_learn_data = pandas.read_csv("./data/words_to_learn.csv")
    words_to_learn = words_to_learn_data.to_dict(orient="records")
except FileNotFoundError:
    # schema - [{'French': 'partie', 'English': 'part'}, {'French': 'histoire', 'English': 'history'}]
    words_to_learn = ORIGINAL_DATA.to_dict(orient="records")
# when user has learned all the words and words_to_learn.csv is empty
except pandas.errors.EmptyDataError:
    words_to_learn = []

# if user knows a word, that has to be removed from words_to_learn
def update_words_to_learn():
    global words_to_learn, known_words

    # while there are words in words_to_learn
    if len(words_to_learn) > 0:
        words_to_learn.remove(current_word)
        words_to_learn_df = pandas.DataFrame(words_to_learn)
        words_to_learn_df.to_csv("./data/words_to_learn.csv", index=False)

        # update the known_words.csv
        known_words.append(current_word)
        known_words_df = pandas.DataFrame(known_words)
        try:
            pandas.read_csv("./data/known_words.csv")
        except FileNotFoundError:
            known_words_df.to_csv("./data/known_words.csv", index=False)
        except pandas.errors.EmptyDataError:
            known_words_df.to_csv("./data/known_words.csv", index=False)
        else:
            known_words_df.to_csv("./data/known_words.csv", index=False, header=False, mode="a")

    next_card()

# ---------------------------- FUNCTIONALITY SETUP ------------------------------- #
def next_card():
    global flip_timer, current_word

    # cancel the previous window.after() when button is clicked
    window.after_cancel(flip_timer)
    window.after_cancel(timer)

    # if there are words in words_to_learn
    if len(words_to_learn) > 0:
        current_word = random.choice(words_to_learn)
        word_in_french = current_word["French"]
        canvas.itemconfig(card_title, text="French", fill="black")
        canvas.itemconfig(card_word, text=word_in_french, fill="black")
        time_keeper(WAIT_SECONDS)
        flip_timer = window.after(WAIT_SECONDS * 1000, flip_card, current_word["English"])
    # if there are no words in words_to_learn
    else:
        canvas.itemconfig(card_title, text="🏆", fill="black", font=("Arial", 30, "bold"))
        canvas.itemconfig(card_word, text="You learnt all the words!", fill="black", font=("Arial", 30, "bold"))

    canvas.itemconfig(canvas_image, image=card_image_front)


def time_keeper(seconds):
    global timer
    if seconds >= 0:
        canvas.itemconfig(card_timer, text=f"Revealing in: 0{seconds}")
        timer = window.after(1000, time_keeper, seconds - 1)

def flip_card(word_in_english):
    canvas.itemconfig(canvas_image, image=card_image_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=word_in_english, fill="white")

# when there are no words in words_to_learn, user can reset the game
# or user can reset the game in between to remove all the words in known_words and fetch original_data to words_to_learn
def reset():

    # show alert to get user confirmation to reset the game
    user_response = messagebox.askyesno("Flashy", "Do you want to reset the game and start fresh?")

    if user_response:
        global words_to_learn
        words_to_learn = ORIGINAL_DATA.to_dict(orient="records")
        words_to_learn_df = pandas.DataFrame(words_to_learn)
        words_to_learn_df.to_csv("./data/words_to_learn.csv", index=False)

        # if the known_words.csv exists, open it, retain the columns, and delet the data
        try:
            known_words_data = pandas.read_csv("./data/known_words.csv")
        except FileNotFoundError:
            pass
        except pandas.errors.EmptyDataError:
            pass
        else:
            # clearing the known_words csv file, but preserve the column headings using.iloc[0:0]
            known_words_data.iloc[0:0].to_csv("./data/known_words.csv", index=False)

        next_card()

# exit the game on click of "Exit Game" button with user confirmation
def exit_game():
    user_confirmation = messagebox.askyesno("Flashy", "Are you sure you want to exit the game?")
    if user_confirmation:
        window.destroy()
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
timer = window.after(3000, time_keeper)


canvas = Canvas(width=600, height=396, bg=BACKGROUND_COLOR, highlightthickness=0)
card_image_front = PhotoImage(file="./images/card_front.png")
card_image_back = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(300, 198, image=card_image_front)
card_title = canvas.create_text(300, 120, text="", font=("Ariel", 35, "italic"))
card_word = canvas.create_text(300, 198, text="", font=("Arial", 50, "bold"))
card_timer = canvas.create_text(480, 350, text=f"Revealing in: 0{WAIT_SECONDS}", font=("Arial", 15, "italic"))
canvas.grid(column=0, row=0, columnspan=2)


wrong_button_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_button_image, borderwidth=0, cursor="hand2", highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

right_button_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_button_image, highlightthickness=0, borderwidth=0, cursor="hand2", command=update_words_to_learn)
right_button.grid(column=1, row=1)

reset_button = Button(text="Reset Game", borderwidth=0, padx=20, pady=4, bg="#728e7f", fg=BACKGROUND_COLOR, font=("Arial", 10, "normal"), cursor="hand2", command=reset)
reset_button.grid(column=0, row=2)

exit_button = Button(text="Exit Game", command=exit_game, padx=20, pady=4, bg="#728e7f", fg=BACKGROUND_COLOR, font=("Arial", 10, "normal"), borderwidth=0, cursor="hand2")
exit_button.grid(column=1, row=2)

def known_words_table():
    new_window = Toplevel(window)

    # create the vertical scroll bar
    y_scroll_bar = ttk.Scrollbar(new_window)
    y_scroll_bar.grid(column=1, row=0, sticky="ns")

    # create the table
    table = ttk.Treeview(new_window, columns=["French", "English"], show="headings", yscrollcommand=y_scroll_bar)
    # bind vertical scroll bar to the table
    y_scroll_bar.config(command=table.yview)

    # create table headings
    table.heading("French", text="French")
    table.heading("English", text="English")
    print(known_words)
    # insert table rows
    for i in range(len(known_words)):
        french_word = known_words[i]["French"]
        english_word = known_words[i]["English"]
        table.insert(parent="", index=i, values=[french_word, english_word])
        print(known_words[i])

    table.grid(column=0, row=0)
    new_window.update_idletasks()
    print(f"{new_window.winfo_width()} x {new_window.winfo_height()}")


see_known_words = Button(text="See Known Words", command=known_words_table)
see_known_words.grid(column=0, row=3)



# to show the 1st word
next_card()
window.mainloop()