import json
import smtplib
from email.message import EmailMessage
from tkinter import *
from tkinter import messagebox
import pandas as pd
import pandas.errors
from customtkinter import CTkTextbox

from sent_emails import show_sent_mails
from customtkinter import *

FONT_LABEL = ("roboto", 14, "normal")
FONT_ENTRY = ("roboto", 14, "normal")
Y_PADDING = 6

SENDER = "vgstcof@gmail.com"
PASSWORD = "fszk cmil iwwt quby"
RECEIVER = "greatbb08@gmail.com"

FILE_NAME = "data_file.csv"
JSON_FILE = "data_file.json"
# ------------------------FUNCTIONALITY SETUP------------------------

def send_email():

    from_id = from_entry.get()
    to_id = to_entry.get()
    subject_text = subject_entry.get()
    body_text = body_entry.get(1.0, END)

    # to check if any field is empty and show alert
    alert_message = "Please enter "
    # flag to check if we have to send mail
    send_mail = True

    if len(from_id) == 0:
        alert_message += "From ID "
        send_mail = False
    if len(to_id) == 0:
        alert_message += "To ID "
        send_mail = False
    if len(subject_text) == 0:
        alert_message += "Subject "
        send_mail = False
    if body_text == "\n":
        alert_message += "Body"
        send_mail = False

    if not send_mail:
        messagebox.showerror("Email Manager", alert_message)
    else:
        # create message to send
        message = EmailMessage()
        message["From"] = from_id
        message["To"] = to_id
        message["Subject"] = subject_text

        # remove the new line char that is at the end of the string
        body_text = body_text.rstrip("\n")
        message.set_content(body_text)

        # 1. create connection
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            # 2. start TLS
            connection.starttls()
            # 3. login
            connection.login(user=SENDER, password=PASSWORD)
            # 4. send email
            connection.send_message(message)

        # clear all data
        # from_entry.delete(0, END)
        # to_entry.delete(0, END)
        # subject_entry.delete(0, END)
        # body_entry.delete(1.0, END)
        new_data = {"from": from_id, "to": to_id, "subject": subject_text, "body": body_text}
        update_data(new_data)




# ------------------------DATA SETUP------------------------

def update_data(new_data):
    # csv route
    # new sent mail data to be added to csv

    # data_df = pd.DataFrame([data])
    # # check if the file exists
    # try:
    #     df = pd.read_csv(FILE_NAME)
    # except FileNotFoundError:
    #     data_df.to_csv(FILE_NAME, index=False)
    # except pandas.errors.EmptyDataError:
    #     data_df.to_csv(FILE_NAME, index=False)
    # else:
    #    #  add the new data at the top of the csv
    #    df = pd.concat([data_df, df], ignore_index=True)
    #    df.to_csv(FILE_NAME, index=False)


    # json route
    try:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # since we are not storing key value pairs, we need list
        data = [new_data]
    else:
        # add new data at the top
        # list is better for this too
        data.insert(0, new_data)

    # Save updated list back to JSON
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)



# ------------------------UI SETUP------------------------

# setup windows
window = CTk()
window.config(padx=20, pady=20)
window.title("Email Manager")

# labels and entry fields
from_label = CTkLabel(master=window, text="From", font=FONT_LABEL)
from_label.grid(column=0, row=0, sticky="w")

from_entry = CTkEntry(master=window, font=FONT_ENTRY)
from_entry.insert(END, SENDER)
from_entry.grid(column=1, row=0, sticky="we", pady=Y_PADDING, ipady=3)

to_label = CTkLabel(master=window, text="To", font=FONT_LABEL)
to_label.grid(column=0, row=1, sticky="w")

to_entry = CTkEntry(master=window, font=FONT_ENTRY)
to_entry.insert(END, RECEIVER)
to_entry.grid(column=1, row=1, sticky="we", pady=Y_PADDING, ipady=3)

subject_label = CTkLabel(master=window, text="Subject", font=FONT_LABEL)
subject_label.grid(column=0, row=2, sticky="w", padx=(0, 10))

subject_entry = CTkEntry(master=window, font=FONT_ENTRY)
subject_entry.grid(column=1, row=2, sticky="we", pady=Y_PADDING, ipady=3)

body_label = CTkLabel(master=window, text="Body", font=FONT_LABEL)
body_label.grid(column=0, row=3, sticky="w")

body_entry = CTkTextbox(master=window, width=300, font=FONT_ENTRY, padx=3, pady=3)
body_entry.grid(column=1, row=3, pady=Y_PADDING)

send_button = CTkButton(master=window, text="Send", cursor="hand2", font=FONT_ENTRY, command=send_email)
send_button.grid(column=1, row=4, pady=Y_PADDING, sticky="w", padx=(Y_PADDING, 0))

sent_mails_button = CTkButton(master=window, text="Sent Emails", cursor="hand2", font=FONT_ENTRY, command=show_sent_mails)
sent_mails_button.grid(column=0, row=4)

# close window button
CTkButton(master=window, text="Close", cursor="hand2", font=FONT_ENTRY, command=window.destroy).grid(column=1, row=4, sticky="e")

window.mainloop()