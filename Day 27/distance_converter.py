from tkinter import *
# distance converter to convert miles to kilometers using tkinter module

FONT = ("Segoe UI", 10, "normal")
MILES_KMS_FACTOR = 1.61

# screen setup
window = Tk()
window.title("Miles to Kms converter")
window.minsize(width=200, height=20)
window.config(padx=10, pady=10)

emoji_label = Label(text="👉", font=FONT)
emoji_label.grid(column=0, row=0)

# text filed to enter the miles to be converted to kms
data_input = Entry(width=7)
data_input.grid(column=1, row=0)

miles_label = Label(text="Miles", font=FONT)
miles_label.grid(column=2, row=0)

text_label1 = Label(text="is equal to")
text_label1.grid(column=0, row=1)

result_label = Label(text="")
result_label.grid(column=1, row=1)

text_label2 = Label(text="km")
text_label2.grid(column=2, row=1)

def miles_to_kms():
    result = round( float(data_input.get()) * MILES_KMS_FACTOR)

    result_label.config(text=result)

button = Button(text="Convert", command=miles_to_kms)
button.grid(column=1, row=2)

window.mainloop()