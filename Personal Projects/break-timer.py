# GOAL - to replicate break timer chrome webstore app
# The app counts from 28 mins to 0 and shows blank screen for 2 minutes for a 30 mins cycle

import customtkinter as ctk
import tkinter as tk

class BreakTimer:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Break Timer")
        # self.app.geometry("300x200")
        self.interval = 5
        self.timer_label = ctk.CTkLabel(self.app, text="27:59", font=("Segoe UI Symbol", 32))
        self.timer_label.grid(row=1, column=1, padx=10, pady=10, columnspan=3)

        # timer control buttons
        self.start_btn = ctk.CTkButton(self.app, text="▶", font=("Segoe UI Symbol", 12), command=lambda: self._counter(self.interval), width=30, fg_color="#0a8e6d", hover_color="#077c5e")
        self.start_btn.grid(row=2, column=1, padx=10, pady=10)
        self.reset_btn = ctk.CTkButton(self.app, text="🔄", font=("Segoe UI Symbol", 12), width=30, fg_color="#242424", border_color="#414449", border_width=1, hover_color="#414449")
        self.reset_btn.grid(row=2, column=2)
        self.quit_btn = ctk.CTkButton(self.app, text="Quit", font=("Segoe UI Symbol", 12), width=60, command=self.app.destroy, fg_color="#242424", border_color="#414449", border_width=1, hover_color="#414449")
        self.quit_btn.grid(row=2, column=3, padx=10)

        self.settings_frame = ctk.CTkFrame(self.app, border_width=1, border_color="#414449")
        self.settings_frame.grid(row=3, column=1, columnspan=3, padx=10, pady=10, ipadx=10, ipady=10)

        self.work_time_entry = ctk.CTkEntry(self.settings_frame, width=60)
        self.work_time_entry.insert(0, "28")
        self.work_time_entry.grid(row=1, column=1, padx=10, sticky="wens")

        self.break_time_entry = ctk.CTkEntry(self.settings_frame, width=60)
        self.break_time_entry.insert(0, "2")
        self.break_time_entry.grid(row=1, column=2, sticky="wens", padx=(0,10))

        self.break_window = None
        self.break_timer_label = None

        self.app.mainloop()


    def _counter(self, interval):
        if interval:
            minutes,seconds = divmod(interval, 60)
            self.timer_label.configure(text=f"{minutes:02.0f}:{seconds:02.0f}")
            self.app.after(1000, lambda: self._counter(interval - 1))
        else:
            self.timer_label.configure(text="00:00")
            self.break_screen()

    def break_screen(self):
        self.break_window = ctk.CTkToplevel()
        self.break_window.title("Break Window")
        self.break_window.geometry(f"{self.break_window.winfo_screenwidth()}x{self.break_window.winfo_screenheight()}+0+0")
        self.break_window.overrideredirect(True)
        self.break_window.attributes("-topmost", True)
        self.break_timer_label = ctk.CTkLabel(self.break_window, text="02:00", font=("Segoe UI Symbol", 32))
        self.break_timer_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        skip_btn = ctk.CTkButton(self.break_window, text="Skip", command= self.break_window.destroy)
        skip_btn.place(relx=0.5, rely=0.57, anchor=tk.CENTER)
        self.break_counter(1*60)

    def break_counter(self, interval):
        if interval:
            minutes, seconds = divmod(interval, 60)
            self.break_timer_label.configure(text=f"{minutes:02.0f}:{seconds:02.0f}")
            self.app.after(1000, lambda: self.break_counter(interval-1))
        else:
            self.break_window.destroy()

breakTimer = BreakTimer()
