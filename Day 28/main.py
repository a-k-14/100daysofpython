from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 5
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
# to reset the timer
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps

    window.after_cancel(timer)
    reps = 0
    status_label.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    completed_checks.config(text="")
    start_button.config(state="normal")

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    # reps to track work, short break, long break and checks
    reps += 1

    start_button.config(state="disabled")

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # model: 4 reps of 25min work - 3 reps of 5min short break, then 20min long break
    # rep 1/3/5/7 - work, rep 2/4/6 - short break, rep 8 - long break
    if reps == 8:
        counter(long_break_sec)
        # print("Work -> Long Break")
        status_label.config(text="Break(20)", fg=RED)
    elif reps % 2 == 0:
        counter(short_break_sec)
        status_label.config(text="Break(5)", fg=PINK)
    elif reps % 2 != 0:
        counter(work_sec)
        status_label.config(text="Work(25)", fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def counter(count):
    if count >= 0:
        minutes = count // 60
        # count % 60 also gives use seconds
        seconds = count - minutes * 60
        # to avoid showing "5:0" or "4:9"
        # we can also use dynamic typing here
        # leading_zero = "0" if seconds < 10 else ""
        canvas.itemconfig(timer_text, text=f"{minutes:02d}:{seconds:02d}")
        # to enable us to reset the counter when we click reset btn
        global timer
        timer = window.after(1000, counter, count - 1)
    # we check reps < 8 here, otherwise it will continue to run indefinitely
    elif reps < 8:
        start_timer()
        # show check mark for every completed work session
        # work session = 1 run of work min + 1 run of break
        if reps % 2 == 0:
            # print(f"reps inside elif= {reps}")
            completed_checks["text"] = "✔" * int(reps / 2)

    # pop up the window when the counter has less than 10 sec
    if count <=10:
        window.lift()
        window.attributes('-topmost', True)
        window.attributes('-topmost', False)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=10, pady=20, bg=YELLOW)

# we set width here to avoid window resizing when text changes from 'Work' -> 'Short Break'
status_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 30, "bold"), width=10)
status_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, highlightthickness=0, bg=YELLOW)
bg_image = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=bg_image)
timer_text = canvas.create_text(100, 130, text="00:00", font=(FONT_NAME, 35, "bold"), fill="white")
canvas.grid(column=1, row=1)

start_button = Button(text="Start", borderwidth=0, padx=5, pady=2, bg="#379b46", fg="white",  font=("Arial", 10, "bold"), command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", borderwidth=0, padx=5, pady=2, bg="#f26849", fg="white", font=("Arial", 10, "bold"), command=reset_timer)
reset_button.grid(column=2, row=2)

completed_checks = Label(bg=YELLOW, fg=GREEN, font=("arial", 12, "bold"))
completed_checks.grid(column=1, row=3)


window.mainloop()