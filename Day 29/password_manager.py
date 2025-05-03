# import all classes and constants in tkinter
import csv # to read the data from passwords.txt and show them
from tkinter import *
from tkinter import messagebox
from prettytable import PrettyTable # to show passwords as a table
from tkinter import simpledialog # to show dialog box to set the key to unlock the passwords
import random # for password generator
import pyperclip # to copy the password to clipboard

# ---------------------------- CONSTANTS ------------------------------- #
FONT = ("Roboto", 11, "normal")
BACKGROUND = "#26282e"
BUTTON_BACKGROUND = "#541c17"
TITLE = "Personal Password Manager"

# A password generator app using python tkinter

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # pick letters on random
    random_letters = [random.choice(letters) for _ in range(0, random.randint(6, 9))]

    # pick symbols on random
    random_symbols = [random.choice(symbols) for _ in range(0, random.randint(2, 4))]

    # pick numbers on random
    random_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password = random_letters + random_symbols + random_numbers
    random.shuffle(password)

    password_entry.delete(0, END)
    password_entry.insert(END, "".join(password))
    pyperclip.copy("".join(password))

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_creds():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # check for missing data
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(TITLE, message="Please enter all the details!")
    else:

        # confirm to save to the login credentials
        save_or_now = messagebox.askokcancel(title=f"Details for {website}", message=f"These are the details entered: \nWebsite: {website} \nEmail/Username: {email} \nPassword: {password} \n\nContinue to save?")
        # tkinter.messagebox.showinfo("1", "2")

        # save if user clicks yes
        if save_or_now:
            with open(file="passwords.txt", mode="a") as file:
                file.write(f"{website} | {email} | {password}\n")

            # show update status
            status_label["text"] = f"Added login details for {website} 🔑"

            # destroy the status after 2 seconds
            # we set text="" instead of destroy, as destroy resizes the window since the status_label s completely removed from window
            # Added window.geometry() to lock the width and height, so using destroy again
            # changed to .config() as destroying the status_label throws error on saving for 2nd time as the widget would have been removed from the window completely
            window.after(3000, lambda: status_label.config(text=""))

            # clear fields
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title(TITLE)
window.config(padx=20, pady=10, bg=BACKGROUND)

canvas = Canvas(width=200, height=200, bg=BACKGROUND, highlightthickness=0)
logo = PhotoImage(file="./logo.png")
canvas.create_image(200/2, 200/2, image=logo)
canvas.grid(column=1, row=0)


website_label = Label(text="Website:", font=FONT, bg=BACKGROUND, fg="white")
website_label.grid(column=0, row=1, sticky="w")

website_entry = Entry(font=FONT)
website_entry.grid(column=1, row=1, columnspan=2, sticky="we")
website_entry.focus()

email_label = Label(text="Email?Username:", font=FONT, pady=5, bg=BACKGROUND, fg="white")
# add padx here to add padding on th right side
# added only for this label as this is the lengthiest label and pushes all entry fields to right
email_label.grid(column=0, row=2, sticky="w", padx=(0, 5))

email_entry = Entry(font=FONT)
email_entry.grid(column=1, row=2, columnspan=2, sticky="we")
# add default value
email_entry.insert(0, "ak14@gmail.com")

password_label = Label(text="Password:", font=FONT, bg=BACKGROUND, fg="white")
password_label.grid(column=0, row=3, sticky="w")

password_entry = Entry(font=FONT)
password_entry.grid(column=1, row=3, sticky="we", padx=(0, 10))

generate_button = Button(text="Generate Password", borderwidth=0, padx=5, pady=1, font=FONT, bg=BUTTON_BACKGROUND, fg="white", command=password_generator)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", padx=2, pady=1, font=FONT, borderwidth=0, bg=BUTTON_BACKGROUND, fg="white", command=save_creds)
add_button.grid(column=1, row=4, columnspan=2, sticky="we", pady=5)

status_label = Label(bg=BACKGROUND, fg="#a4acc6", font=FONT)
status_label.grid(column=0, row=5, columnspan=3, sticky="we", pady=10)

# Lock the window size to prevent resizing
# window.update_idletasks()  # Ensure all widgets are rendered
# print(f"{window.winfo_width()} x {window.winfo_height()}")
# window.geometry(f"{window.winfo_width()}x{window.winfo_height()}")


# ---------------------------- DISPLAY PASSWORDS ------------------------------- #

# GOAL - show the saved passwords as a scrollable list when the key is entered

# check if the key entered is correct and show the passwords as a table inside the text widget
# after showing the passwords, change the button text to lock and when the button is clicked again
# lock - clear table, change button text to unlock
def lock_unlock_creds():
    # could be "Unlock" or "Lock"
    unlock_button_state = unlock_button["text"]

    # passwords are not shown yet
    if unlock_button_state == "Unlock":

        # get the key in the stored file
        with open("key.txt") as file:
            stored_key = file.read()

        entered_key = key_entry.get()

        if len(entered_key) == 0:
            messagebox.showerror(TITLE, "Please enter the key to unlock passwords!")
        elif entered_key != stored_key:
            messagebox.showerror(TITLE, "Please enter the correct key!")
        elif entered_key == stored_key:

            unlock_button.config(text="Lock")

            # delete the key from entry field
            key_entry.delete(0, END)

            # get the password from the file
            with open(file="passwords.txt", mode="r") as passwords_file:
                reader = csv.reader(passwords_file, delimiter="|")

                # table to show the data in a tabular format
                table = PrettyTable()
                # column headings
                table.field_names = ["Website", "Email/Username", "Password"]

                # add passwords to the table
                for row in reader:
                    # row structure -> ['wed ', ' ak14@gmail.com ', ' ewd']
                    table.add_row([f"{row[0].strip()}", f"{row[1].strip()}", f"{row[2].strip()}"], divider=True)


                # sort the data by website name and get the table as a string as text widget of tkinter accepts only strings
                my_str = table.get_string(sortby="Website")
                # add the table string to text field
                passwords_display_text.insert(END, my_str)
            return
    elif unlock_button_state == "Lock":
        passwords_display_text.delete(1.0, END)
        unlock_button.config(text="Unlock")
        messagebox.showinfo(TITLE, "Passwords locked!")


key_label = Label(text="Key to show passwords: ", bg=BACKGROUND, fg="white", font=FONT)
key_label.grid(column=0, sticky="w", row=6, pady=(0, 10))

key_entry = Entry(bg="#1e1f22", font=FONT, fg="white")
key_entry.grid(column=1, row=6, sticky="we", pady=(0, 10))

unlock_button = Button(text="Unlock", bg=BUTTON_BACKGROUND, fg="white", borderwidth=0, font=FONT, command=lock_unlock_creds)
unlock_button.grid(column=2, row=6, sticky="we", padx=(10, 0), pady=(0, 10))

# scroll bar to scroll the passwords shown in the txt field
vbar = Scrollbar()
# sticky = "nse": ns -> to stretch top to bottom, e -> to stick to the right corner of the column
vbar.grid(column=3, sticky="nse", row=7)

passwords_display_text = Text(width=15, height=8, yscrollcommand=vbar.set, bg="#1e1f22", fg="white", borderwidth=0)
passwords_display_text.grid(column=0, sticky="we", columnspan=3, row=7, padx=(0, 3))

vbar.config(command=passwords_display_text.yview)

# ---------------------------- KEY SETUP ------------------------------- #
# GOAL - At the start of the app, to check if the key to unlock passwords is set or not
# If not set, show a dialog box to set the same before continuing with the app

# func to set the key
# user has to mandatorily set the key, so we prompt till the key is set
def set_key():

    while True:
        user_key = simpledialog.askstring(TITLE, "Set the key to unlock passwords:       ")
        if user_key:
            with open(file="key.txt", mode="w") as key_file:
                key_file.write(user_key)
            return


# we use this to create the file on the very 1st run of the app to ensure we do not get error when we open key.txt and check if key exists
# if key does not exist i.e. user_ket len() is 0, call set_key()
# we implemented try except block
# with open(file="key.txt", mode="a") as f:
#     pass

# on every run, we check if the key exists in the key.txt file
# with open("key.txt") as file:
#     key = file.read()
#     if len(key) == 0:
#         set_key()
#
try:
    file = open(file="key.txt", mode="r")
except FileNotFoundError:
    set_key()


# to change the password unlock key
change_key_button = Button(text="Change Key", borderwidth=0, bg=BUTTON_BACKGROUND, fg="white", command=set_key)
change_key_button.grid(column=2, row=8, sticky="e")

window.mainloop()