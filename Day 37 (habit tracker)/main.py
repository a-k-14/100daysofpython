import tkcalendar as tkc # to display calendar to pick the date
import customtkinter as ctk # for better UI
import datetime as dt # to format the selected date and to enable today in today_btn
from data import *
from tkinter.messagebox import showinfo

# creating a custom button class as we use the same design for 4 buttons
class CustomGreyButton(ctk.CTkButton):
    def __init__(self, master, text, command, width=140):
        super().__init__(
        master= master,
        fg_color = "transparent",
        text_color = "#a4a4a4",
        border_width = 1,
        border_color = "#515151",
        hover_color = "#282828",
        text = text,
        command = command,
        width = width
        )


ctk.set_appearance_mode("dark")
# ctk.set_default_color_theme("blue")

# main window of the app
root = ctk.CTk()
# root.geometry("313x460")
# disable resize on vertical and horizontal axis
root.resizable(False, False)
root.title("Habit Tracker")

# frame to hold habit manage ui
manage_habit_frame = ctk.CTkFrame(master=root)
manage_habit_frame.grid(column=0, row=0, padx=20, pady=(20, 10), sticky="we", columnspan=2)
# to ensure columns stretch to the available space
manage_habit_frame.grid_columnconfigure(0, weight=1)
manage_habit_frame.grid_columnconfigure(1, weight=1)

# title of habit manage frame
# 777777
select_habit_label = ctk.CTkLabel(master=manage_habit_frame, text="Select Habit", font=(None, 18, "bold"),
                                  text_color="#5c5c5c")
select_habit_label.grid(column=0, row=0, pady=10, padx=10)

# dropdown menu to choose the habit
option_menu_choices = ["Walking", "Coding", "Running", "Sleep"]
def option_menu_callback(choice):
    print(choice)
habit_selector = ctk.CTkOptionMenu(master=manage_habit_frame, values=option_menu_choices,
                                   command=option_menu_callback,
                                   )
# set default choice
habit_selector.set(option_menu_choices[1])
habit_selector.grid(column=1, row=0, padx=(0,10))

# to manage habits - create new habits, delete existing habits
manage_habits_btn = CustomGreyButton(master=manage_habit_frame, text="Manage Habits",
                                     command=lambda: print("Manage Habit button clicked!"))
manage_habits_btn.grid(column=0, row=2, padx=(10, 10), pady=(0, 10), columnspan=2, sticky="we")


# calendar frame to contain calendar, data entry, buttons
main_ui_frame = ctk.CTkFrame(root)
main_ui_frame.grid(column=0, row=1, padx=20, pady=(0,20), sticky="we")

# we have a separate frame just for the calendar to set wh (width & height) for calendar
# tkc does not have wh properties for calendar
calendar_frame = ctk.CTkFrame(main_ui_frame, fg_color="blue")
calendar_frame.grid(column=0, row=0, padx=10, pady=10, columnspan=2, sticky="w")

# function to update UI and perform other actions on date change in calendar
def date_changed(_):
    # get the date selected
    selected_date = calendar.selection_get()

    #---------Update selected_date_label---------
    # we need to show the selected date in selected_date_label as Mon day year weekday
    # we can use strftime method
    # since that works only on datetime obj, we convert selected date to datetime obj
    datetime_obj = dt.date.fromisoformat(f"{selected_date}") # gives datetime object of a date passed as string
    selected_date_label.configure(text=format_selected_date(datetime_obj))

    # print(dt.date.fromisoformat(f"{selected_date}").strftime("%b %d %Y %a"))


# calendar to pick date
calendar = tkc.Calendar(master=calendar_frame, cursor="hand2",  showweeknumbers=False, bordercolor="#252526",
                        font=(None, 13), locale="en_IN",
                        normalforeground= "#e5e5e5", normalbackground = "#252526",
                        othermonthforeground="grey", othermonthbackground="#252526",
                        weekendforeground= "white", weekendbackground="#252526",
                        othermonthweforeground="grey", othermonthwebackground="#252526",
                        headersforeground="#e2e2e2", headersbackground="#373737",
                        )
calendar.grid(column=0, row=0, sticky="nsew", columnspan=2)
calendar.bind("<<CalendarSelected>>", date_changed)

# As tkc does not have wh properties, we can set the wh for calendar_frame and use sticky="nsew" for calendar
# But, the wh of parent (i.e. calendar_frame) are decided by the wh of the children (i.e. child calendar)
# Though CTkFrame (calendar_frame) have default w=200, h=200 properties, these are used only when the parent frame does not have any children
# we can set the following to False that ensures parent's wh are not dependent on the children
calendar_frame.grid_propagate(False)
# Since parent's (i.e. calendar_frame) wh is not based on child (i.e. calendar), the following wh will take effect
# though we are setting default values, this is to show our wh values will take effect now
calendar_frame.configure(width=200)
# we also need to set the following to tell tkinter that the resp. column and row should stretch to fill the available space
calendar_frame.grid_columnconfigure(0, weight=1)
calendar_frame.grid_rowconfigure(0, weight=1)
# to make sure the calendar sticks to right (i.e. 'e'), we have to set this
main_ui_frame.grid_columnconfigure(0, weight=1)
# we are setting the weight for 2nd column also to ensure update_btn & delete_btn take same width
# without the weight for 2nd column (i.e. index=1), update_btn in column=0 takes longer width
main_ui_frame.grid_columnconfigure(1, weight=1)

# func to format the selected date label
def format_selected_date(date: dt):
    return date.strftime("%b\n%d\n%Y\n%a")

# label to show the selected day details next to the calendar widget and above the today button
selected_date_label = ctk.CTkLabel(main_ui_frame, text=format_selected_date(calendar.selection_get()), text_color="#5c5c5c", font=(None, 18, "bold"))
selected_date_label.grid(column=1, row=0, sticky="e", padx=10)

# to set the calendar to today's date on click of today_btn
def set_to_today():
    today = dt.datetime.now()
    calendar.selection_set(dt.date(today.year, today.month, today.day))
    # also show the today's date in the selected_date_label
    selected_date_label.configure(text=format_selected_date(today))

# button to go to today when navigated to a different month/year
today_btn = CustomGreyButton(master=main_ui_frame, text="Today", width=40, command= set_to_today)
today_btn.grid(column=1, row=0, sticky="es", pady=10, padx=10)

# control entry label text length so that it will not affect the window size
def set_label_text(text, max_length):
    return text if len(text) <= max_length else text[:max_length-4] + " ..."

# to add the habit value for the selected day
entry_label = ctk.CTkLabel(main_ui_frame, text=set_label_text("Minutes", 15), text_color="#5c5c5c", font=(None, 18, "bold"), width=100, anchor="w")
entry_label.grid(column=0, row=1, padx=10)

entry = ctk.CTkEntry(main_ui_frame, text_color="#e5e5e5", width=100)
entry.grid(column=1, row=1, padx=(0,10), sticky="we")

# success - 457a4a
# failure - b54747
status_label = ctk.CTkLabel(main_ui_frame, text="", font=(None, 18, "bold"), text_color="#457a4a")

# to hide the status label and show the entry field back
def hide_status():
    status_label.grid_forget()
    entry.grid(column=1, row=1, padx=(0,10), sticky="we")

def add_data():

    # return if the entry field is empty
    entry_data = entry.get()

    if len(entry_data) <= 0:
        showinfo(title="Habit Tracker", message="Please enter the value to add.")
        return

    # get the selected date
    selected_date = calendar.selection_get()
    # print(selected_date)
    # pass on date to update the graph and get the response
    response = graph_update(date=f"{selected_date}", quantity=entry_data)

    # configure the status label
    if response == 200:
        status_label.configure(text="Success", text_color="#457a4a")
        # empty the entry field only if the update was successful, else retain it so that user can retry
        entry.delete(0, "end")
        set_to_today()
    else:
        status_label.configure(text="Try Again!", text_color="#b54747")

    # hide entry field, show status label for 1 second and then hide it, then un hide entry field
    add_btn.configure(state="disabled")
    entry.grid_forget()
    status_label.grid(column=1, row=1)
    root.after(1500, hide_status)
    add_btn.configure(state="normal")

# button to add the habit details for the selected day
add_btn = ctk.CTkButton(main_ui_frame, text="Add", command=add_data)
add_btn.grid(column=0, row=2, sticky="we", padx=10, pady=10, columnspan=2)

# update and delete buttons to alter the habit details for the selected day
update_btn = CustomGreyButton(master=main_ui_frame, text="Update", width=120,
                              command= lambda: print("Update Button clicked!"))
update_btn.grid(column=0, row=3, padx=10, sticky="we")

# function to delete the data for selected date if it exists
def delete_data():
    selected_date = calendar.selection_get()
    response = delete_pixel(date=f"{selected_date}")

    # configure the status label
    if response == 200:
        status_label.configure(text="Success", text_color="#457a4a")
        set_to_today()
    else:
        status_label.configure(text="Try Again!", text_color="#b54747")

    # hide entry field, show status label for 1 second and then hide it, then unhide entry field
    delete_btn.configure(state="disabled")
    entry.grid_forget()
    status_label.grid(column=1, row=1)
    root.after(1500, hide_status)
    delete_btn.configure(state="normal")

delete_btn = CustomGreyButton(master=main_ui_frame, text="Delete", width=120, command= delete_data)
delete_btn.grid(column=1, row=3, padx=(0,10), sticky="we")

# button to view the graph
view_habit_btn = ctk.CTkButton(main_ui_frame, text="View Habit", command=view_graph)
view_habit_btn.grid(column=0, row=4, sticky="we", padx=10, pady=10, columnspan=2)

# to exit the app
exit_btn = CustomGreyButton(master=root, text="Exit", command= root.destroy)
exit_btn.grid(column=0, columnspan=2, row=2, sticky="we", padx=20, pady=(0,10))


# root.update()
# w=472 x h=762
# print(f"w={root.winfo_width()} x h={root.winfo_height()}")

root.mainloop()