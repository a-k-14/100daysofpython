import customtkinter as ctk
import tkinter as tk
import time

# set theme of the app
ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("Task Timer")

# --- Define Global Variables for Timer ---
running = False
start_time = 0
paused_time = 0
total_paused_duration = 0
timer_id = None

# --- Grid Configuration ---
app.grid_columnconfigure(0, weight=0)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)
app.grid_columnconfigure(3, weight=1)


# option menu to choose the task
def option_menu_callback(choice):
    print("Selected:", choice)


task_option_menu = ctk.CTkComboBox(app, values=["100 days of python ", "IIMBAA", "PDS", "PYL", "100 days of python",
                                                "IIMBAA", "PDS", "PYL", "100 days of python 100 days of python",
                                                "IIMBAA", "PDS", "PYL", "PYL"], command=option_menu_callback,
                                   state="readonly")
task_option_menu.grid(row=1, column=1, padx=10, pady=10, columnspan=3, sticky="we")

# widget to show the running timer
timer_var = tk.StringVar()
timer_text = "00:00:00"
timer_var.set(timer_text)
timer_entry = ctk.CTkEntry(app, textvariable=timer_var, font=("Segoe UI Symbol", 35, "bold"), justify="center",
                           text_color="#9e9e9e", state="disabled")
timer_entry.grid(row=2, column=1, columnspan=3, sticky="we", padx=10, pady=10)

notes_entry = ctk.CTkTextbox(app, text_color="#f2f2f2", height=65, width=180, font=('Segoe UI', 14),
                             border_color="#4c5154", border_width=1)
notes_entry.grid(row=3, column=1, sticky="we", padx=10, pady=10, columnspan=3)


# --- Timer Functions (as before) ---
def update_timer():
    global start_time, running, total_paused_duration, timer_id
    if running:
        elapsed_seconds = (time.time() - start_time) - total_paused_duration
        hours, remainder = divmod(int(elapsed_seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        timer_var.set(f"{hours:02}:{minutes:02}:{seconds:02}")
        timer_id = app.after(1000, update_timer)


def start_timer_action():
    global running, start_time, paused_time, total_paused_duration, timer_id
    if not running:
        if timer_id: app.after_cancel(timer_id)
        if paused_time > 0:
            total_paused_duration += (time.time() - paused_time); paused_time = 0
        else:
            start_time = time.time(); total_paused_duration = 0
        running = True;
        start_btn.configure(text="⏸", fg_color="#FBC02D");
        update_timer()
        print("Timer Started/Resumed")
    else:
        running = False;
        paused_time = time.time();
        start_btn.configure(text="▶", fg_color="#085bbe")
        if timer_id: app.after_cancel(timer_id)
        print("Timer Paused")


def stop_timer_action():
    global running, start_time, paused_time, total_paused_duration, timer_id
    if running or paused_time > 0:
        if timer_id: app.after_cancel(timer_id)
        elapsed_seconds = (time.time() - start_time) - total_paused_duration
        print(f"Task ended. Total time: {int(elapsed_seconds)} seconds.")
        running = False;
        start_time = 0;
        paused_time = 0;
        total_paused_duration = 0;
        timer_id = None;
        timer_var.set("00:00:00")
        start_btn.configure(text="▶", fg_color="#085bbe")
    print("Stopped")


def reset_timer_action():
    global running, start_time, paused_time, total_paused_duration, timer_id
    if timer_id: app.after_cancel(timer_id)
    running = False;
    start_time = 0;
    paused_time = 0;
    total_paused_duration = 0;
    timer_id = None;
    timer_var.set("00:00:00")
    start_btn.configure(text="▶", fg_color="#085bbe")
    print("Timer Reset")


start_btn = ctk.CTkButton(app, text="▶", command=start_timer_action, cursor="hand2",
                          font=("Segoe UI Symbol", 16, "bold"), width=40, fg_color="#085bbe")
start_btn.grid(row=4, column=1, padx=10, pady=10, sticky="we")

stop_btn = ctk.CTkButton(app, text="⏹", cursor="hand2", font=("Segoe UI Symbol", 16), width=40,
                         command=stop_timer_action, fg_color="#C62828")
stop_btn.grid(row=4, column=2, sticky="we")

reset_btn = ctk.CTkButton(app, text="Reset", cursor="hand2", command=reset_timer_action, width=60, fg_color="#242424",
                          border_color="#414449", border_width=1)
reset_btn.grid(row=4, column=3, padx=10, pady=10, sticky="we")

# Ensure all widget geometries are processed before getting sizes/setting final window geometry
app.update_idletasks()

# --- Position Window in Bottom-Right (WITH DPI ADJUSTMENT AND BOTTOM MARGIN) ---
app_width = 240
app_height = 280
margin = 20  # No right margin for now

screen_width_logical = app.winfo_screenwidth()
screen_height_logical = app.winfo_screenheight()

# Calculate logical X, Y
x_pos_logical = screen_width_logical - app_width - margin

# Adjust for overflow by setting a small margin from the bottom
# This 'bottom_margin_logical' value is in logical pixels.
# You might need to fine-tune this value (e.g., try 10, 15, 20, 25, 30)
bottom_margin_logical = 85  # Start with 20 logical pixels (30 physical)

y_pos_logical = screen_height_logical - app_height - bottom_margin_logical

# Apply DPI scaling factor
dpi_scale_factor = 1.5

# Convert logical coordinates to physical for geometry()
x_pos_physical = int(x_pos_logical * dpi_scale_factor)
y_pos_physical = int(y_pos_logical * dpi_scale_factor)

# --- DEBUGGING PRINTS ---
print(f"\n--- Positioning Debug (Final Adjustment) ---")
print(f"Screen Width (logical): {screen_width_logical}")
print(f"Screen Height (logical): {screen_height_logical}")
print(f"App Width (configured): {app_width}")
print(f"App Height (configured): {app_height}")
print(f"Margin (right): {margin}")
print(f"Bottom Margin (logical): {bottom_margin_logical}")
print(f"Logical X Position: {x_pos_logical}")
print(f"Logical Y Position: {y_pos_logical}")
print(f"DPI Scale Factor: {dpi_scale_factor}")
print(f"Adjusted Physical X Position: {x_pos_physical}")
print(f"Adjusted Physical Y Position: {y_pos_physical}")
print(f"Geometry string: {app_width}x{app_height}+{x_pos_physical}+{y_pos_physical}")
print(f"--------------------------------------------------\n")

# Set the window's geometry and position
app.geometry(f"{app_width}x{app_height}+{x_pos_physical}+{y_pos_physical}")
app.resizable(False, False)

app.mainloop()
