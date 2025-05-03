##################### Extra Hard Starting Project ######################
import datetime # to get today's date
import pandas as pd # to read csv into dict
import random # to pick random letter template
import smtplib # to send email
from email.message import EmailMessage # to construct message to be sent via mail

SENDER = "vgstcof@gmail.com"
PASSWORD = "fszk cmil iwwt quby"

# 1. Update the birthdays.csv
# done
# 2. Check if today matches a birthday in the birthdays.csv
# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
# 4. Send the letter generated in step 3 to that person's email address.

# function to get the random letter
def get_letter():
    # pick a random letter
    letter_num = random.randint(1, 3)

    # open letter
    with open(f"letter_templates/letter_{letter_num}.txt") as f:
        # read the contents of the letter
        letter = f.read()
        return letter


# function to send wishes
def send_wishes(name, to_id):
    # get a random letter from the list of letters
    letter = get_letter()
    # replace [NAME] in the letter with the name of the person to be wished
    letter = letter.replace("[NAME]", name)

    # setup message to be sent
    message = EmailMessage()
    message["From"] = SENDER
    message["To"] = to_id
    message["Subject"] = "Birthday Wishes"
    # set body
    message.set_content(letter)

    # 1. create connection
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        # 2. start TLS
        connection.starttls()
        # 3. login
        connection.login(user=SENDER, password=PASSWORD)
        # 4. send email
        connection.send_message(message)


# get the data from the csv
df = pd.read_csv("birthdays.csv")
data_dict = df.to_dict(orient="records")
print(type(data_dict))
print(data_dict)

# get today's date
today_date = datetime.date.today().day

# check if birthday date matches today's date
# and trigger wishes to be sent
for item in data_dict:
    birthday_date = item["day"]
    if birthday_date == today_date:
        send_wishes(item["name"], item["email"])
