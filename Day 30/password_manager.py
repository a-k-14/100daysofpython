# import all classes and constants in tkinter
from tkinter import *
from tkinter import messagebox
from prettytable import PrettyTable # to show passwords as a table
from tkinter import simpledialog # to show dialog box to set the key to unlock the passwords
import random # for password generator
import pyperclip # to copy the password to clipboard
import json # to store the passwords in a json file instead of txt

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
    website = website_entry.get().lower()
    email = email_entry.get()
    password = password_entry.get()

    # check for missing data
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(TITLE, message="Please enter all the details!")
    else:
        # confirm to save to the login credentials
        save_yes_or_no = messagebox.askokcancel(title=f"Details for {website}", message=f"These are the details entered: \nWebsite: {website} \nEmail/Username: {email} \nPassword: {password} \n\nContinue to save?")

        # save if user clicks yes
        if save_yes_or_no:

            # create a dict for newly entered data
            new_data = {
                website:
                    {
                        "email": email,
                        "password": password,
                    }
            }

            try:
                # if the passwords.json already exists, open and load(read) the existing data
                with open("passwords.json", "r") as data_file:
                    # read old data in the json
                    data = json.load(data_file)
            except FileNotFoundError:
                # if passwords.json does not exist, then create it and dump(write) new_data
                with open("passwords.json", "w") as data_file:
                    # saving the 1st entry
                    json.dump(new_data, data_file, indent=4)
            else:
                # if passwords.json exists, update it with the new_data
                data.update(new_data)
                with open("passwords.json", "w") as data_file:
                    # saving the updated data
                    json.dump(data, data_file, indent=4)
            finally:
                # show update status
                status_label["text"] = f"Added login details for {website} 🔑"
                # remove update status after 3 seconds
                window.after(3000, lambda: status_label.config(text=""))

                # clear fields
                website_entry.delete(0, END)
                password_entry.delete(0, END)

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_creds():
    search_term = website_entry.get()

    # 1st try using if...else, and if that is not possible only then use try...except
    try:
        with open("passwords.json") as data_file:
            data = json.load(data_file)
            # search_result = data[search_term.lower()]
    except FileNotFoundError:
        message = "No passwords saved so far."
    else:
        if search_term.lower() in data:
            search_result = data[search_term.lower()]
            message = f"Here are the details for {search_term} \nEmail: {search_result['email']} \nPassword: {search_result['password']}"
        else:
            message = f"Did not find the details for '{search_term}'"
    finally:
        messagebox.showinfo(TITLE, message)


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
website_entry.grid(column=1, row=1, sticky="we", padx=(0, 5))
website_entry.focus()

search_button = Button(text="Search", borderwidth=0, bg=BUTTON_BACKGROUND, fg="white", padx=5, pady=2, command=search_creds, cursor="hand2")
search_button.grid(column=2, row=1, sticky="we")

email_label = Label(text="Email?Username:", font=FONT, pady=5, bg=BACKGROUND, fg="white")
email_label.grid(column=0, row=2, sticky="w", padx=(0, 10))

email_entry = Entry(font=FONT)
email_entry.grid(column=1, row=2, columnspan=2, sticky="we")
# add default value
email_entry.insert(0, "ak14@gmail.com")

password_label = Label(text="Password:", font=FONT, bg=BACKGROUND, fg="white")
password_label.grid(column=0, row=3, sticky="w")

password_entry = Entry(font=FONT)
password_entry.grid(column=1, row=3, sticky="we", padx=(0, 5))

generate_button = Button(text="Generate Password", borderwidth=0, padx=5, pady=1, font=FONT, bg=BUTTON_BACKGROUND, fg="white", command=password_generator, cursor="hand2")
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", padx=2, pady=1, font=FONT, borderwidth=0, bg=BUTTON_BACKGROUND, fg="white", command=save_creds, cursor="hand2")
add_button.grid(column=1, row=4, columnspan=2, sticky="we", pady=5)

status_label = Label(bg=BACKGROUND, fg="#a4acc6", font=FONT)
status_label.grid(column=0, row=5, columnspan=3, sticky="we", pady=10)


# ---------------------------- DISPLAY PASSWORDS ------------------------------- #
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
            # delete the key from entry field
            key_entry.delete(0, END)

            # to catch the error if the passwords.json does not exist
            try:
                # get the passwords from the file
                with open(file="passwords.json", mode="r") as passwords_file:
                    data = json.load(passwords_file)
            except FileNotFoundError:
                passwords_display_text.delete(1.0, END)
                passwords_display_text.insert(END, "No passwords to display")
            else:
                unlock_button.config(text="Lock")

                # table to show the data in a tabular format
                table = PrettyTable()
                # column headings
                table.field_names = ["Website", "Email/Username", "Password"]

                # add passwords to the table
                for key in data:
                    table.add_row([f"{key}", f"{data[key]['email']}", f"{data[key]['password']}"], divider=True)

                # sort the data by website name and get the table as a string as text widget of tkinter accepts only strings
                my_str = table.get_string(sortby="Website")
                # add the table string to text field
                passwords_display_text.insert(END, my_str)
    elif unlock_button_state == "Lock":
        passwords_display_text.delete(1.0, END)
        unlock_button.config(text="Unlock")
        messagebox.showinfo(TITLE, "Passwords locked!")


key_label = Label(text="Key to show passwords: ", bg=BACKGROUND, fg="white", font=FONT)
key_label.grid(column=0, sticky="w", row=6, pady=(0, 10))

key_entry = Entry(bg="#1e1f22", font=FONT, fg="white")
key_entry.grid(column=1, row=6, sticky="we", pady=(0, 10))

unlock_button = Button(text="Unlock", bg=BUTTON_BACKGROUND, fg="white", borderwidth=0, font=FONT, command=lock_unlock_creds, cursor="hand2")
unlock_button.grid(column=2, row=6, sticky="we", padx=(10, 0), pady=(0, 10))

# scroll bar to scroll the passwords shown in the txt field
vbar = Scrollbar()
# sticky = "nse": ns -> to stretch top to bottom, e -> to stick to the right corner of the column
vbar.grid(column=3, sticky="nse", row=7)

passwords_display_text = Text(width=15, height=8, yscrollcommand=vbar.set, bg="#1e1f22", fg="white", borderwidth=0)
passwords_display_text.grid(column=0, sticky="we", columnspan=3, row=7, padx=(0, 3))

vbar.config(command=passwords_display_text.yview)

# ---------------------------- KEY SETUP ------------------------------- #
def set_key():

    while True:
        user_key = simpledialog.askstring(TITLE, "Set the key to unlock passwords:       ")
        if user_key:
            with open(file="key.txt", mode="w") as key_file:
                key_file.write(user_key)
            return


try:
    file = open(file="key.txt", mode="r")
except FileNotFoundError:
    set_key()


# to change the password unlock key
change_key_button = Button(text="Change Key", borderwidth=0, bg=BUTTON_BACKGROUND, fg="white", command=set_key, cursor="hand2")
change_key_button.grid(column=2, row=8, sticky="e")

window.mainloop()