import customtkinter as ctk
import tkinter as tk # You'll still need tkinter for StringVar

# Assuming 'app' is already initialized and configured
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Task Timer")
# ... (your existing app setup code) ...


# Initial list of tasks (you can load this from Excel)
# For demonstration, let's use a sample list
initial_tasks = ["100 days of python", "IIMBAA", "PDS", "PYL"]

def option_menu_callback(choice):
    """Callback for when an item is selected from the dropdown."""
    print("Selected from dropdown:", choice)

def add_task_on_enter(event):
    """
    Function to add the typed task to the combobox's options
    when the Enter key is pressed.
    """
    # Get the text currently in the combobox entry part
    typed_task = task_option_menu.get().strip() # .strip() removes leading/trailing whitespace

    if typed_task: # Check if the typed text is not empty
        # Get the current list of values from the combobox
        current_values = list(task_option_menu.cget("values"))

        if typed_task not in current_values:
            # If the task is new, add it to the list
            current_values.append(typed_task)
            current_values.sort() # Optional: keep the list sorted alphabetically

            # Update the combobox with the new list of values
            task_option_menu.configure(values=current_values)

            # Optionally, set the combobox's current value to the newly added task
            # task_option_menu.set(typed_task)

            print(f"Added new task: '{typed_task}' to the list.")
        else:
            print(f"Task '{typed_task}' already exists in the list.")
    else:
        print("Empty task entered. No task added.")

# Your CTkComboBox setup:
task_option_menu = ctk.CTkComboBox(
    app,
    values=initial_tasks, # Start with your initial list
    command=option_menu_callback,
    state="normal" # IMPORTANT: Change state to "normal" to allow typing
)
task_option_menu.set("")
task_option_menu.grid(row=1, column=1, padx=10, pady=5, columnspan=3, sticky="we")

# Bind the <Return> (Enter key) event to the combobox
# This means when the combobox is focused and Enter is pressed,
# the 'add_task_on_enter' function will be called.
task_option_menu.bind("<Return>", add_task_on_enter)

label = ctk.CTkLabel(app, text="Type new task and press Enter", font=("Segoe UI", 12, "bold"), height=1, text_color="#7a848d")
label.grid(row=2, column=1, padx=10)
# You would then have the rest of your app's widgets and logic...
app.mainloop()

