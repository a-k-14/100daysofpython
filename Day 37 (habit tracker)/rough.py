import tkinter as tk
from tkcalendar import Calendar, DateEntry

window = tk.Tk()

def date_entry_selected(event):
    w = event.widget
    date = w.get_date()
    print('Selected Date:{}'.format(date))
    # <ref to Calendar>.calevent_create(date, 'Hello ...`)
    cal.calevent_create(date, 'Hello ...', "Hey")

cal = Calendar(window, selectmode='day', year=2025, month=5, day=5)
cal.pack(fill="both", expand=True)

de=DateEntry(window)  
de.pack()  
de.bind("<<DateEntrySelected>>", date_entry_selected)  
window.mainloop()
