import tkinter
from tkinter import ttk
import json
import tkinter.scrolledtext as st

JSON_FILE = "data_file.json"
FONT_DATA = ("roboto", 15, "normal")

# ------------------------DATA SETUP------------------------
def get_data():
    try:
        with open(JSON_FILE) as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = "No Mails Sent"

    return data

# ------------------------UI SETUP------------------------

# popup to show sent mail details
def display_popup(details: dict):
    # x & y padding for display elements
    padding_units = 10

    popup = tkinter.Toplevel()
    popup.title("Email Details")
    # print(details["from"])

    # UI setup to show sent mail details
    tkinter.Label(popup, text="From", font=FONT_DATA).grid(column=0, row=0, sticky="w", padx=padding_units, pady=padding_units)
    tkinter.Label(popup, text=details.get("from", "NA"), font=FONT_DATA).grid(column=1, row=0, sticky="w")

    tkinter.Label(popup, text="To", font=FONT_DATA).grid(column=0, row=1, sticky="w", padx=padding_units, pady=padding_units)
    tkinter.Label(popup, text=details.get("to", "NA"), font=FONT_DATA).grid(column=1, row=1, sticky="w")

    tkinter.Label(popup, text="Subject", font=FONT_DATA).grid(column=0, row=2, sticky="w", padx=padding_units, pady=padding_units)
    tkinter.Label(popup, text=details.get("subject", "NA"), font=FONT_DATA).grid(column=1, row=2, sticky="w")

    tkinter.Label(popup, text="Body", font=FONT_DATA).grid(column=0, row=3, sticky="w", padx=padding_units, pady=padding_units)
    # tkinter.Label(popup, text=details.get("body", "NA")).grid(column=1, row=3, sticky="w")

    # body_text = tkinter.Text(popup, wrap=tkinter.WORD, width=50, height=10)
    # body_text.insert("end", details.get("body", "NA"))
    # body_text.config(state="disabled")
    # body_text.grid(column=1, row=3, padx=padding_units)

    body_text1 = st.ScrolledText(popup, width=50, height=10, font=FONT_DATA, wrap=tkinter.WORD)
    body_text1.insert("end", details.get("body", "NA"))
    body_text1.config(state= "disabled")
    body_text1.grid(column=1, row=3, ipadx=10, ipady=10)


    tkinter.Button(popup, text="Close", highlightthickness=0, cursor="hand2", command= popup.destroy, font=FONT_DATA).grid(column=0, row=4, columnspan=2, pady=padding_units)

def show_sent_mails():
    window = tkinter.Toplevel()
    window.title("Sent Mails")

    column_headings = ("To", "Subject...", "Message...")
    table = ttk.Treeview(window, columns=column_headings, show="headings", cursor="hand2")

    # configure the font size for columns
    style = ttk.Style()
    style.configure("Treeview.Heading", font=FONT_DATA)
    style.configure("Treeview", font=FONT_DATA, rowheight=50)

    # setup column headings
    for heading in column_headings:
        # format -> table.heading(column: "To", option: "To")
        table.heading(heading, text=heading)

    # set column width of columns
    table.column(f"{column_headings[1]}", width=300)
    table.column(f"{column_headings[2]}", width=500)

    # show sent mails data
    sent_mails_data = get_data()

    # dict to store the full sent mail data to be shown in a new window
    full_data = {}

    for item in sent_mails_data:
        # show to id excl domain name after @
        to = item["to"]
        to = to.partition("@")[0]

        # show first 20 characters of the text
        subject = item["subject"]
        subject = subject[0:20] + "..." if len(subject) > 20 else subject

        # show first 30 characters of text and replace new line "\n" with space
        body = item["body"]
        body = body[0:50].replace("\n", " ") + "..." if len(body) > 50 else body

        # we use this id as key in the full_data dict to store full data
        line_id = table.insert(parent="", index=tkinter.END, values=(to, subject, body))

        full_data[line_id] = item

    # to show the full details of sent mail details
    # here event is pointless, so we use _
    def show_details(_):
        # get the index of the 1st item in selected items
        selected_index = table.selection()[0]
        #get the full data from full_data dict
        details = full_data[selected_index]
        display_popup(details)

    # # cursor changes on hover
    # table.bind("<Enter>", lambda e: table.config(cursor="hand2"))
    # table.bind("<Leave>", lambda e: table.config(cursor="hand2"))

    # Interaction bindings - show details on lmb single click
    table.bind("<<TreeviewSelect>>", show_details)

    # setup vertical scrollbar for the table
    y_scroll_bar = ttk.Scrollbar(window, command=table.yview)
    table.config(yscrollcommand=y_scroll_bar)

    table.grid(column=0, row=0, sticky="nsew")
    y_scroll_bar.grid(column=1, row=0, sticky="ns")


    # button to close the window
    tkinter.Button(window, text="Close", highlightthickness=0, cursor="hand2", command=window.destroy, font=FONT_DATA).grid(column=0, row=1, columnspan=2, pady=10)

    window.mainloop()