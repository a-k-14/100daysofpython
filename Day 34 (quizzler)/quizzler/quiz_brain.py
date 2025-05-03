class QuizBrain:

    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        # to track incorrect answers to be recorded in csv log via exit_with_log method in ui.py
        self.incorrect_answers = 0
        self.question_list = q_list
        self.number_of_questions = len(self.question_list)
        self.current_question = None

    def still_has_questions(self):
        return self.question_number < self.number_of_questions

    def next_question(self):
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        return f"Q.{self.question_number}: {self.current_question.text}"
        # user_answer = input(f"Q.{self.question_number}: {self.current_question.text} (True/False): ")
        # self.check_answer(user_answer)

    def check_answer(self, user_answer):
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        else:
            self.incorrect_answers += 1
            return False
