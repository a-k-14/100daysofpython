# GOAL
# a time tracker app
# user to select the task from a task list drop down (data source for task list -> excel)
# has buttons -> start, pause, end, reset
# stores the start time, end time in Excel on click of end button
# resets timer on reset button click

import customtkinter as ctk
import tkinter as tk


class TaskTimer():
    def __init__(self) -> None:
        # set the window theme to 'dark' mode
        ctk.set_appearance_mode("dark")
        # initialize the main window
        self.app = ctk.CTk()
        self.app.title("Task Timer")
        # disable window resizing
        self.app.resizable(False, False)
        self.task_list = [" <Add new task...>", "100 days of python", "IIMBAA", "PDS", "PYL", "100 days of python", "IIMBAA", "PDS", "PYL", "100 days of python 100 days of python", "IIMBAA", "PDS", "PYL", "IIMBAA", "PDS", "PYL"]

        # declared it here as these are used by multiple methods
        self.task_list_menu = None
        self.new_task_status_label = None
        self.start_btn = None
        self.notes_entry = None
        # build the ui (widgets) of the app
        self.build_ui()

        # to store the after() ID and to handle .after() calls overlaps
        self.status_update_queue = None
        # position app window in the bottom right corner of the screen
        self.position_window()
        self.app.mainloop()

    def list_menu_callback(self, choice):
        # instead of removing the existing task manually, if any
        # select the " <Add new task...>" item to clear the field and set the focus to type the new task
        # space before < to ensure this stays at the top after sorting the list
        if choice == " <Add new task...>":
            self.task_list_menu.set("")
            self.task_list_menu.focus()
        else:
            # to remove the blinking cursor in the combobox after item selection
            self.app.focus()
        print("Selected Task:", choice)


    def update_task_status_label(self, status: str):
        """
        Display status of task addition on press of enter key in new_task_status_label, for 3 seconds
        :param status: str ["Added", "Exists!", "Empty!"]
        """
        # check if a status update task is running and cancel it before starting a new task
        if self.status_update_queue is not None:
            self.app.after_cancel(self.status_update_queue)

        # show the task addition status
        if status != "Added":
            self.new_task_status_label.configure(text=status, text_color="#b54747")
        else:
            self.new_task_status_label.configure(text=status, text_color="#009933")

        # schedule a new status update task to hide the status and store the ID
        # schedule task only if the status is not empty, else it will lead to infinite loop
        # Call 1 ("Added") → Call 2 ("") → Call 3 ("") → Call 4 ("") → ...
        if status:
            self.status_update_queue = self.app.after(10000, lambda: self.update_task_status_label(""))


    def add_task_on_enter(self, event):
        """
        Function to add a new task typed into the task_list_menu combobox, and on press of 'Enter' key
        """
        # get the text currently in the combobox entry
        # .strip() removes leading/trailing whitespace
        # converted to 'str' to enable capitalization
        new_task = self.task_list_menu.get().strip().capitalize()

        # if the new_task is not empty and does not exist in the task_list, add it to the task_list
        if new_task:
            if new_task not in self.task_list:
                self.task_list.append(new_task)
                self.task_list.sort()
                # update the combobox with the new task_list
                self.task_list_menu.configure(values=self.task_list)
                # set the value to new_task with spaces stripped and capitalized
                self.task_list_menu.set(new_task)
                # show the task addition status
                self.update_task_status_label("Added")
                # to remove focus (cursor) from the task_list_menu combobox
                self.app.focus()
            else:
                self.update_task_status_label("Exists!")
        else:
            self.update_task_status_label("Empty!")


    def run_timer(self):
        if self.start_btn.cget("text") == "▶":
            self.start_btn.configure(text="⏸")
            print("Timer running")
        else:
            self.start_btn.configure(text="▶")
            print("Timer paused")


    def end_timer(self):
        if self.start_btn.cget("text") == "⏸":
            self.start_btn.configure(text="▶")
        print("Timer stopped")


    def reset_timer(self):
        if self.start_btn.cget("text") == "⏸":
            self.start_btn.configure(text="▶")
        print("Timer reset")


    def build_ui(self):
        # dropdown menu to choose the tasks from task_list
        self.task_list_menu = ctk.CTkComboBox(self.app, values=self.task_list, command=self.list_menu_callback)
        self.task_list_menu.grid(row=1, column=1, padx=10, pady=(10, 3), sticky="we", columnspan=3)
        # remove the default option displayed from combobox dropdown (defaults to the first option)
        self.task_list_menu.set("")
        # to add a new task and press of the Enter key
        self.task_list_menu.bind("<Return>", self.add_task_on_enter)

        # hint text to show how to add a new task to the task_list
        hint_label = ctk.CTkLabel(self.app, text="Type new task & press Enter", font=("Segoe UI", 12, "bold"), height=5, text_color="#7a848d")
        hint_label.grid(row=2, column=1, columnspan=3, padx=10, sticky="w")

        # status text to show a message on task addition
        # 009933 07b17b
        self.new_task_status_label = ctk.CTkLabel(self.app, text="", text_color="#009933", font=("Segoe UI", 12, "bold"), height=5)
        self.new_task_status_label.grid(row=2, column=3, sticky="e", padx=(0, 12))

        # entry widget to display the running timer
        # to set initial text
        initial_timer_var = tk.StringVar()
        initial_text = "10:12:09"
        initial_timer_var.set(initial_text)
        timer_display = ctk.CTkEntry(self.app, textvariable=initial_timer_var, height=75, font=("Segoe UI Symbol", 40, "bold"), justify="center", state="disabled", text_color="#9e9e9e")
        timer_display.grid(row=3, column=1, columnspan=3, padx=10, pady=10, sticky="we")

        # field to enter notes for the task
        self.notes_entry = ctk.CTkTextbox(self.app, text_color="#f2f2f2", width=220, height=65, font=("Segoe UI", 14), border_width=1, border_color="#4c5154")
        self.notes_entry.grid(row=4, column=1, columnspan=3, sticky="we", padx=10)

        # buttons to control the functionality
        self.start_btn = ctk.CTkButton(self.app, text="▶", command=self.run_timer, cursor="hand2", width=40, font=("Segoe UI Symbol", 16, "bold"), fg_color="#085bbe")
        self.start_btn.grid(padx=10, row=5, column=1, sticky="we", pady=10)

        end_btn = ctk.CTkButton(self.app, text="⏹", width=40, cursor="hand2", font=("Segoe UI Symbol", 16, "bold"), fg_color="#085bbe", command=self.end_timer)
        end_btn.grid(row=5, column=2, sticky="we")

        reset_btn = ctk.CTkButton(self.app, text="Reset", cursor="hand2", width=60, fg_color="#242424", border_color="#414449", border_width=1, command=self.reset_timer)
        reset_btn.grid(padx=10, row=5, column=3, sticky="we")


    def position_window(self):
        # -----------positioning window in the bottom right corner of the screen-----------
        self.app.update_idletasks()

        # Logical vs. Physical Pixels: Screen operates at a physical pixel resolution of 1920x1080, but with 150% DPI scaling, Windows presents a "logical" resolution 1280x720 to applications
        # The coordinates passed to geometry() for positioning might be interpreted as physical pixels by the OS, even if Tkinter is internally working with logical pixels.
        # Solution: By taking the logical positions, multiplying them by dpi_scale_factor (1.5), and then passing those x_pos_physical and y_pos_physical values to app.geometry(), we ensure the window is placed at the correct physical coordinates - bottom right corner

        # position the app window in the bottom right corner of the screen with a margin
        right_margin = 20
        # separate bottom margin to offset the taskbar height
        bottom_margin = 80
        # by trial and error, found app wxh = 240x280 as app.winfo_width() and app.winfo_height() were not giving correct dimensions, probably due to DPI scaling
        app_width = 240
        app_height = 280

        dpi_scale_factor = 1.5

        screen_width_logical = self.app.winfo_screenwidth()
        screen_height_logical = self.app.winfo_screenheight()

        # calculate the logical x y coordinates
        x_logical = screen_width_logical - app_width - right_margin
        y_logical = screen_height_logical - app_height - bottom_margin

        # convert logical coordinates to physical for .geometry()
        x_physical = int(x_logical * dpi_scale_factor)
        y_physical = int(y_logical * dpi_scale_factor)

        # set the app window's position
        self.app.geometry(f"+{x_physical}+{y_physical}")


app = TaskTimer()