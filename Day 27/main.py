from tkinter import *

window = Tk()
window.title("GUI with tkinter")
window.minsize(width=500, height=300)
window.config(pady=10, padx=10)

label = Label(text="Enter something in the input filed", font=("Arial", 12, "bold"))
# label.pack()
# label.place(x=400, y=200)
label.grid(column=0, row=0)

my_input = Entry()
# my_input.pack()
my_input.grid(column=1, row=1)

def button_click():
    label.config(text=my_input.get())

button = Button(text="Click to update", command=button_click)
# button.config(padx=20, pady=20)
# button.pack()
button.grid(column=2, row=2)



window.mainloop()