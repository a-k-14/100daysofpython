import tkinter as tk
import datetime as dt
import pandas as pd
import os

from quiz_brain import QuizBrain

THEME_COLOR = "#375362"
# to cancel previous action of window.after()
# process_queue = ""

class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        # start date and time to log into csv in exit_with_log func
        now = dt.datetime.now()
        self.date = now.strftime("%A %d-%m-%Y")
        self.start_time = now.strftime("%I:%M:%S %p")

        self.window = tk.Tk()
        self.window.title("Quizzler")
        self.window.config(bg=THEME_COLOR, padx=20, pady=20)

        self.score_label = tk.Label(text="Score: 0", bg=THEME_COLOR, fg="white", font=("roboto", 14, "normal"))
        self.score_label.grid(column=1, row=0, sticky="e")

        self.canvas = tk.Canvas(width=300, height=250)
        self.question_text = self.canvas.create_text(300/2, 250/2, text="Question...", font=("Arial", 16, "italic"), width=280)
        self.canvas.grid(column=0, row=1, pady=20, columnspan=2)

        true_bg = tk.PhotoImage(file="./images/true.png")
        self.true_btn = tk.Button(image=true_bg, cursor="hand2", command= lambda: self.button_pressed("True"))
        self.true_btn.grid(column=0, row=2, sticky="w")

        false_bg = tk.PhotoImage(file="./images/false.png")
        self.false_btn = tk.Button(image=false_bg, cursor="hand2", command= lambda: self.button_pressed("False"))
        self.false_btn.grid(column=1, row=2, sticky="e")

        self.exit_btn = tk.Button(text="Exit Game", cursor="hand2", bg=THEME_COLOR, borderwidth=0, font=("roboto", 12, "normal"), activebackground=THEME_COLOR, fg="white", command= self.exit_with_log)
        self.exit_btn.grid(column=0, row=3, columnspan=2, pady=(10,0))

        # to get the 1st question
        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        # get new question only if there are questions in the list
        # i.e. if the question number < 10 as we call API for 10 Qs

        self.canvas.config(bg="white")
        # print("From get_next_question")

        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}/{self.quiz.number_of_questions}")
            next_q = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=next_q)
            self.true_btn.config(state="active")
            self.false_btn.config(state="active")
        else:
            self.canvas.itemconfig(self.question_text, text="End of Quiz...")
            self.true_btn.config(state= "disabled")
            self.false_btn.configure(state= "disabled")

    # check the answer on button press
    def button_pressed(self, option: str):
        is_right = self.quiz.check_answer(option)
        self.give_feedback(is_right)


    # to show the green or red bg as feedback to the user
    def give_feedback(self, is_right: bool):
        # global process_queue
        # print("From give_feedback")
        # try :
        #     self.window.after_cancel(process_queue)
        # except ValueError:
        #     pass
        # if the answer is right i.e. is_right = True, show green bg
        # else show red bg
        # after 1 sec delay, show next Q, and change bg to white

        # disabling buttons to prevent rapid inputs
        self.true_btn.config(state="disabled")
        self.false_btn.config(state="disabled")

        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")

        self.window.update()
        process_queue = self.window.after(400, self.get_next_question)

    # function to exit game and also log data (start date, start time, no of questions from API, correct questions, incorrect questions, no of questions played, end time) to a csv
    def exit_with_log(self):
        log_data = {
            "date": self.date,
            "start_time": self.start_time,
            "end_time": dt.datetime.now().strftime("%I:%M:%S %p"),
            "questions_from_api": self.quiz.number_of_questions,
            "played_questions": self.quiz.score + self.quiz.incorrect_answers,
            "correct": self.quiz.score,
            "incorrect": self.quiz.incorrect_answers
        }

        log_df = pd.DataFrame([log_data])

        log_file = "quizzler_log.csv"

        # try:
        #     pd.read_csv(log_file)
        # except (FileNotFoundError, pd.errors.EmptyDataError):
        #     log_df.to_csv(log_file, index=False)
        # else:
        #     log_df.to_csv(log_file, mode="a", index=False, header=False)

        # check if the file exists and the file is not empty
        # if os.path.exists(log_file) and os.stat(log_file).st_size != 0:
        #     log_df.to_csv(log_file, mode="a", index=False, header=False)
        # else:
        #     log_df.to_csv(log_file, index=False)

        # we need header only if the file is not there or file is empty
        log_df.to_csv(log_file,
                      mode="a",
                      index=False,
                      header= not (os.path.exists(log_file) and os.stat(log_file).st_size != 0)
                      )


        print(log_data)
        self.window.destroy()
