# GOAL
# to send alerts on mail to the users

import smtplib
from email.message import EmailMessage
import locale

TIME_ZONE = "Asia/Kolkata"
SENDER = "vgstcof@gmail.com"
PASSWORD = "fszk cmil iwwt quby"

def send_mail(receiver, message_content):
    message = EmailMessage()
    message["From"] = SENDER
    message["To"] = receiver
    message["Subject"] = "Time to pack your bags🧳. We have a new deal🛫"
    message.set_content(message_content)

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=SENDER, password=PASSWORD)
        connection.send_message(message)
    print(f"Mail sent to {receiver}")


def send_alerts(users, offers):
    message = "Hola! \n\nHere are the best deals for your next trip:\n\n"

    locale.setlocale(locale.LC_MONETARY, "en_IN")
    # print(offers)

    for offer in offers:
        # format price to Indian number format
        price_inr = locale.currency(offer["price_inr"], grouping=True)

        data = f'''{offer['origin_city']} ({offer['origin_iatacode']}) -> {offer['destination_city']} ({offer['destination_iatacode']})
on: {offer['journey_date']}, at: {offer['journey_time']} 
for: {price_inr}
{offer['mode']} | {offer['route']}\n\n'''

        message += data

    message += "\nCiao👋"

    for user in users:
        send_mail(receiver=user["whatIsYourEmailId?"], message_content=message)
