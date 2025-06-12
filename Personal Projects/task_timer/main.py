# GOAL
# a time tracker app
# user to select the task from a task list drop down (data source for task list -> excel)
# has buttons -> start, pause, end, reset
# stores the start time, end time in Excel on click of end button
# resets timer on reset button click

import customtkinter as ctk
import os
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.utils.exceptions import InvalidFileException
import datetime as dt
from enum import Enum

class TimerStatus(Enum):
    # to track the timer status for the buttons to work correctly
    RUNNING = 1
    PAUSED = 2
    STOPPED = 3

class TaskTimer:
    def __init__(self) -> None:
        # set the window theme to 'dark' mode
        ctk.set_appearance_mode("dark")
        # initialize the main window
        self.app = ctk.CTk()
        self.app.title("Task Timer")
        # disable window resizing
        self.app.resizable(False, False)

        # Excel file to store the task list, time
        self.excel_file = "Task_Timer.xlsx"
        # Sheet in the Excel file to store the task list
        self.excel_tasks_sheet = "Tasks"
        # name of the column storing tasks inside the Tasks sheet
        self.tasks_col_name = "Tasks"
        # Sheet in the Excel file to store the time for each task
        self.excel_time_sheet = "Time"
        # get the task list from the Excel if it exists, to populate task_list_menu combobox dropdown
        self.task_list = self._get_task_list()
        # task selected from the task_list_menu combobox
        self.current_task = ""
        # track the timer status - running, paused, stopped
        self.is_timer_running: TimerStatus = TimerStatus.STOPPED
        # to display timer text inside the timer_display Entry
        self.timer_text = ctk.StringVar()
        # to track the number of seconds elapsed and to use to set the text for timer_display Entry via timer_text
        self.seconds_elapsed = 0
        self.start_time = None # to store the start time of the task
        self.end_time = None # to store the end time of the task

        # declared it here as these are used by multiple methods
        self.task_list_menu = None
        self.new_task_status_label = None
        self.timer_display = None
        self.start_btn = None
        # Textbox for user to type in task notes
        self.notes_entry = None
        # build the ui (widgets) of the app
        self.build_ui()

        # to store the after() ID and to handle .after() calls overlaps i.e., to be used in .after_cancel()
        self.status_update_queue = None
        # self.timer_running_queue = None
        # position app window in the bottom right corner of the screen
        self.position_window()
        self.app.mainloop()


    def _get_task_list(self):
        """
        Read tasks from the Excel file if it exists and is not empty
        Only includes tasks where Status='Active'
        :returns list: A list of tasks always starting with "<Add new task...>".
        Returns just ["<Add new task...>"] if the Excel file doesn't exist, is empty, or has invalid data.
        """

        tasks_list = []

        # 1. check if the file exists and is not empty
        if os.path.exists(self.excel_file) and os.path.getsize(self.excel_file) > 0:
            # to catch errors in reading the file
            try:
                # 2. read the Excel sheet into a DF
                tasks_df = pd.read_excel(self.excel_file, sheet_name=self.excel_tasks_sheet)
                # print(f"tasks df:\n{tasks_df}")

                # 3. check if DF is not empty (e.g., only headers)
                if not tasks_df.empty:
                    # 4. drop blanks in 'Tasks' column and filter out tasks with status != 'active'
                    active_tasks = tasks_df[
                        tasks_df[self.tasks_col_name].notna() &
                        (tasks_df["Status"].str.lower() == "active")
                    ]

                    # 5. convert the tasks to a list
                    tasks_list = active_tasks[self.tasks_col_name].to_list()
                    tasks_list.sort()

                else:
                    print(f"{self.excel_file} exists but contains no data.")
            except pd.errors.ParserError as e:
                print(f"Error reading the file to get the task list: {e}")
            except Exception as e:
                # catch any other unexpected errors
                print(f"An unexpected error occurred while getting the task list: {e}")
        else:
            print(f"{self.excel_file} doesn't exist or is empty.")

        # print(f"{tasks_list=}")
        return ["<Add new task...>"] + tasks_list


    def list_menu_callback(self, choice):
        # instead of removing the existing task manually, if any,
        # user can select the "<Add new task...>" item to clear the field and set the focus to type the new task
        # space before < to ensure this stays at the top after sorting the list
        if choice == "<Add new task...>":
            self.task_list_menu.set("")
            self.task_list_menu.focus()
        else:
            # set the current task value
            self.current_task = choice
            # to remove the blinking cursor in the combobox after item selection
            self.app.focus()
        # print("Selected Task:", choice)


    def _update_task_status_label(self, status: str, code: int):
        """
        Display status of a task for 3-seconds
        :param status: str
        :param code: int | 0 for success 1 for failure/error/warning
        """
        # check if a status update task is running and cancel it before starting a new task
        if self.status_update_queue is not None:
            self.app.after_cancel(self.status_update_queue)

        # show the task addition status
        if code == 1:
            # if there is an error/failure
            status = status + " :(" if status else status
            self.new_task_status_label.configure(text=status, text_color="#b54747")
        else:
            # if the task is successful
            status = status + " :)" if status else status
            self.new_task_status_label.configure(text=status, text_color="#009933")

        # schedule a new status update task to hide the status and store the ID
        # schedule task only if the status is not empty, else it will lead to infinite loop
        # Call 1 ("Added") → Call 2 ("") → Call 3 ("") → Call 4 ("") → ...
        if status:
            self.status_update_queue = self.app.after(3000,
                                                      lambda: self._update_task_status_label("", 1)
                                                      )


    def _append_data_to_excel(self, sheet_name, **kwargs) -> bool:
        """
        Appends new row of data to the specified sheet in the Excel file
        Creates the Excel file/new sheet if they don't exist
        Data is passed as keyword arguments and keywords become headers
        Example usage:
            _append_data_to_excel("Tasks", Task="Study Python", Status="Active", Added_On="2025-04-05 10:00")
            _append_data_to_excel("Time", Task="Study Python", Timestamp="2025-04-05 10:00", Notes="Great progress!")
        :param sheet_name: (str): Name of the sheet to append to
        :param kwargs: Each key becomes a column header, value becomes cell data
        :returns bool: True if successful, False otherwise
        """
        # using openpyxl for appending data as calculating last row (with openpyxl) is required for pandas
        try:
            # 1. check if the file exists or to be created
            if os.path.exists(self.excel_file):
                try:
                    # Attempt to load the workbook. This will fail for zero-byte or corrupted files
                    wb = load_workbook(self.excel_file)
                except (InvalidFileException, Exception) as e:
                    print(f"Error with existing file: {e}. Creating new file.")
                    wb = Workbook()
                    # remove default sheets created e.g., 'Sheet1'
                    if len(wb.sheetnames) > 0:
                        for s in wb.sheetnames:
                            wb.remove(wb[s])
            else:
                # file does not exist, so creating a new file
                wb = Workbook()
                # remove default sheets created e.g., 'Sheet1'
                if len(wb.sheetnames) > 0:
                    for s in wb.sheetnames:
                        wb.remove(wb[s])

            # 2. check if the sheet exists or to be created
            if sheet_name not in wb.sheetnames:
                sheet = wb.create_sheet(sheet_name)
                # set the headings for the sheet
                sheet.append(list(kwargs.keys()))
            else:
                # sheet exists in the Excel file
                sheet = wb[sheet_name]

            # 3. append the new data
            sheet.append(list(kwargs.values()))

            # 4. save and close the Excel file
            wb.save(self.excel_file)
            wb.close()
            return True
        except Exception as e:
            # This outer catch is for errors during sheet creation, appending, or saving
            print(f"Error on appending data to excel: {e}")
            return False


    def _add_task_on_enter(self, event):
        """
        To add a new task typed into the task_list_menu combobox to the task_list and Excel, on press of 'Enter' key
        """
        # get the text currently in the combobox entry
        # .strip() removes leading/trailing whitespace
        new_task = self.task_list_menu.get().strip()

        # if the new_task is not empty and does not exist in the task_list, add it to the task_list
        if new_task:
            # to preserve formats like 'ITR' 'GPS'
            new_task = new_task[0].upper() + new_task[1:]
            if new_task not in self.task_list:
                # add/append the task to excel and if that is successful, proceed further
                now = dt.datetime.now()
                write_status = self._append_data_to_excel(self.excel_tasks_sheet, Tasks=new_task, Status="Active", Added_On = f"{now:%b %d, %Y T%I:%M %p}")

                # perform further steps
                if write_status:
                    self.task_list = self._get_task_list()
                    # to ensure "<Add new task...>" is at the top of the list
                    self.task_list[1:] = sorted(self.task_list[1:])
                    # update the combobox with the new task_list
                    self.task_list_menu.configure(values=self.task_list)
                    # set the value to new_task with spaces stripped and capitalized
                    self.task_list_menu.set(new_task)
                    # update the current task selection which will be used as validation for starting timer on click of start_btn in run_timer method
                    self.current_task = new_task
                    # show the task addition status
                    self._update_task_status_label("Added", 0)
                    # to remove focus (cursor) from the task_list_menu combobox
                    self.app.focus()
                else:
                    self._update_task_status_label("Error", 1)
            else:
                self._update_task_status_label("Exists", 1)
        else:
            self._update_task_status_label("Empty", 1)


    def _update_timer(self):
        # recursively count seconds and update timer text as long as the timer is running
        if self.is_timer_running == TimerStatus.RUNNING:
            self.seconds_elapsed += 1
            # print(f"_update_timer {self.seconds_elapsed=}")
            hours_elapsed, remainder = divmod(self.seconds_elapsed, 3600)
            # the remainder we get here is the seconds remaining
            minutes_elapsed, remainder = divmod(remainder, 60)
            # show the timer in the timer_display Entry via timer_text instance variable
            self.timer_text.set(f"{hours_elapsed:02}:{minutes_elapsed:02}:{remainder:02}")
            self.app.after(1000, self._update_timer)

    def run_timer(self):
        """
        Handles starting, pausing, resuming timer
        """
        # if self.start_btn.cget("text") == "▶":
        # check if a task is selected before starting the timer
        if self.current_task:
            # run timer if the timer is not running i.e., timer is paused or stopped
            if self.is_timer_running != TimerStatus.RUNNING:
                # we set the start_time before changing the is_timer_running status to catch the scenario where a timer that was paused is being resumed
                # when paused, is_timer_running = PAUSED, so != RUNNING
                # we then set is_timer_running = RUNNING and after that we again set start_time as this inner if evaluates true,
                # i.e., RUNNING != PAUSED which means a new start_time is created for an already running task
                # Set start_time only if the timer is beginning a new session (from STOPPED);
                # this preserves the original start time when resuming from a PAUSED state.
                if self.is_timer_running != TimerStatus.PAUSED:
                    self.start_time = dt.datetime.now()
                self.is_timer_running = TimerStatus.RUNNING
                self.start_btn.configure(text="⏸")
                # to not select a new task while the timer is running
                self.task_list_menu.configure(state="disabled")
                self._update_timer()
                print("Timer running")
            else:
                self.is_timer_running = TimerStatus.PAUSED
                self.start_btn.configure(text="▶")
                # as we are updating self.is_timer_running = TimerStatus.STOPPED, _update_timer() will stop as it runs only when the timer is running -> if self.is_timer_running == TimerStatus.RUNNING: ...
                # self._update_timer()
                print("Timer paused")
        else:
            # if no task is selected before starting the timer (hitting start_btn)
            self._update_task_status_label("Select", 1)
        self.app.focus()


    def _humanize_time(self) -> str:
        """
        Formats the total seconds elapsed (self.seconds_elapsed) into H:MM string format to be used for saving to the Excel
        Handles durations longer than 24 hours by accumulating hours
        Calculates timedelta = end_time - start_time and returns the time difference in a human-readable form - 2h:12m
        :return: str: 2h:12m
        """
        difference = self.end_time - self.start_time
        diff_seconds = difference.total_seconds()
        hours, remainder = divmod(diff_seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        return f"{hours:.0f}h:{minutes:02.0f}m"

    # if there is an error in saving the data to the Excel file (e.g., file is opened and so permission is denied), we have to stop timer and show 'Error' status
    # when user clicks stop_btn again, we have to try saving to the Excel again (e.g., user closed the file now and hit stop_btn again)
    # since we set the running status = STOPPED in the else block also to stop the timer, next time when user clicks stop_btn, we will not try to save the data
    def end_timer(self):
        """
        Stops the timer, saves the task log to Excel, and resets the timer state
        stop timer (_update_timer())
        reset the timer text (timer_text)
        change the timer running status (is_timer_running)
        change the symbol on the start button
        deselect task in task_list_menu
        """
        # if the timer is not stopped i.e., is_timer_status is running/paused
        if self.is_timer_running != TimerStatus.STOPPED:
            self.end_time = dt.datetime.now()
            # write data to the Excel Date, Task, Duration, Notes, Start Time, End Time, Seconds
            # print(f"{self.start_time:%d-%b-%Y}, {self.current_task}, {self._humanize_time()}, {self.notes_entry.get('1.0', 'end-1c')},{self.start_time:%I:%M %p}, {self.end_time:%I:%M %p}, {self.seconds_elapsed}")
            write_status = self._append_data_to_excel(self.excel_time_sheet,
                                       Date=f"{self.start_time:%d-%b-%Y}",
                                       Task=self.current_task,
                                       Duration=self._humanize_time(),
                                       Notes=self.notes_entry.get("1.0", "end-1c"),
                                       Start_Time=f"{self.start_time:%I:%M %p}",
                                       End_Time=f"{self.end_time:%I:%M %p}",
                                       Total_Seconds=self.seconds_elapsed
                                       )
            # show status of saving the data to the Excel file
            if write_status:
                self._update_task_status_label("Saved", 0)
                self.current_task=""
                self.reset_timer()
                # we can't edit combobox when the state is disabled
                # the state is disabled when start_btn is clicked,
                # the state is set to normal inside the reset_timer,
                # so after that we can set the value to "", else this line will have no change
                # Gemini AI or qwen did not catch this
                self.task_list_menu.set("")
                print("Time log saved successfully.")
            else:
                # if failed to save the data to the Excel
                self._update_task_status_label("Error", 1)
                self.is_timer_running = TimerStatus.STOPPED
                print("Error saving the log!")
            # we reset the timer at the last so that seconds_elapsed is not set to 0 in the Excel

        print("Timer stopped")


    def reset_timer(self):
        """
        stop timer
        reset seconds to 0
        change timer running status, stop button symbol
        :return:
        """
        # assume user wants to continue existing the task, but reset the timer
        # so this does not clear the selection in task_list_menu or current_task
        # if the timer is not stopped i.e., running/paused
        if self.is_timer_running != TimerStatus.STOPPED:
            # change the running status
            self.is_timer_running = TimerStatus.STOPPED
            self.seconds_elapsed = 0
            self.start_btn.configure(text="▶")
            self.timer_text.set("00:00:00")
            self.notes_entry.delete("1.0", "end") # clear notes
            # as we are updating self.is_timer_running = TimerStatus.STOPPED, _update_timer() will stop as it runs only when the timer is running
            # self._update_timer()
            self.task_list_menu.configure(state="normal")
            # to remove focus from notes entry field if the notes were being typed
            self.app.focus()
        print("Timer reset")


    def build_ui(self):
        """
        To build the widgets of the app
        """
        # dropdown menu to choose the tasks from task_list
        self.task_list_menu = ctk.CTkComboBox(self.app, values=self.task_list, command=self.list_menu_callback)
        self.task_list_menu.grid(row=1, column=1, padx=10, pady=(10, 3), sticky="we", columnspan=3)
        # remove the default option displayed from combobox dropdown (defaults to the first option)
        self.task_list_menu.set("")
        # to add a new task and press of the Enter key
        self.task_list_menu.bind("<Return>", self._add_task_on_enter)

        # hint text to show how to add a new task to the task_list
        hint_label = ctk.CTkLabel(self.app, text="Type new task & press Enter", font=("Segoe UI", 12, "bold"), height=5,
                                  text_color="#7a848d")
        hint_label.grid(row=2, column=1, columnspan=3, padx=10, sticky="w")

        # status text to show a message on task addition
        # 009933 07b17b
        self.new_task_status_label = ctk.CTkLabel(self.app, text="", text_color="#009933",
                                                  font=("Segoe UI", 12, "bold"), height=5)
        self.new_task_status_label.grid(row=2, column=3, sticky="e", padx=(0, 12))

        # entry widget to display the running timer
        # set initial text
        initial_timer_text= "00:00:00"
        self.timer_text.set(initial_timer_text)
        self.timer_display = ctk.CTkEntry(self.app, textvariable=self.timer_text, height=75,
                                     font=("Segoe UI Symbol", 40, "bold"), justify="center", state="disabled",
                                     text_color="#9e9e9e")
        self.timer_display.grid(row=3, column=1, columnspan=3, padx=10, pady=10, sticky="we")

        # field to enter notes for the task
        self.notes_entry = ctk.CTkTextbox(self.app, text_color="#f2f2f2", width=220, height=65, font=("Segoe UI", 14),
                                          border_width=1, border_color="#4c5154")
        self.notes_entry.grid(row=4, column=1, columnspan=3, sticky="we", padx=10)

        # buttons to control the functionality
        self.start_btn = ctk.CTkButton(self.app, text="▶", command=self.run_timer, cursor="hand2", width=40,
                                       font=("Segoe UI Symbol", 16, "bold"), fg_color="#085bbe")
        self.start_btn.grid(padx=10, row=5, column=1, sticky="we", pady=10)

        end_btn = ctk.CTkButton(self.app, text="⏹", width=40, cursor="hand2", font=("Segoe UI Symbol", 16, "bold"),
                                fg_color="#085bbe", command=self.end_timer)
        end_btn.grid(row=5, column=2, sticky="we")

        reset_btn = ctk.CTkButton(self.app, text="Reset", cursor="hand2", width=60, fg_color="#242424",
                                  border_color="#414449", border_width=1, command=self.reset_timer)
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
