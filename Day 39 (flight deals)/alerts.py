# GOAL
# to send sms and email alerts for low price dates and destinations
import os
from twilio.rest import Client

def send_sms(message_body):
    virtual_num = "+13185438874"
    receiver_num = "+917019467824"
    twilio_account_sid = os.environ["twilio_account_sid"]
    twilio_auth_token = os.environ["twilio_auth_token"]

    client = Client(twilio_account_sid, twilio_auth_token)

    message = client.messages.create(
        body=message_body,
        from_=virtual_num,
        to=receiver_num,
    )

    print(message.body)

