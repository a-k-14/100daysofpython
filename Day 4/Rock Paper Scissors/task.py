import random

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''
choices = [rock, paper, scissors]

user_choice = int(input("What do you choose? (1 - rock, 2 - paper, 3 - scissors) "))
user_choice = user_choice - 1

if user_choice < 0 or user_choice > 2:
    print("Incorrect choice🙄")
    exit()
else:
    print(choices[user_choice])

computer_choice = random.randint(0, len(choices) - 1)
print(f"Computer choose: \n{choices[computer_choice]}")

if user_choice == 0:
    if computer_choice == 1:
        print("Computer wins😭")
    elif computer_choice == 2:
        print("You win😎")
    else:
        print("Tie✋")
elif user_choice == 1:
    if computer_choice == 0:
        print("You win😎")
    elif computer_choice == 1:
        print("Tie✋")
    else:
        print("Computer wins😭")
# user_choice == 2
elif user_choice == 2:
    if computer_choice == 0:
        print("Computer wins😭")
    elif computer_choice == 1:
        print("You win😎")
    else:
        print("Tie✋")
# else:
#     print("Tie✋")

