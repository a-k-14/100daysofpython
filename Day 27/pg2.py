from tkinter import *


# create the window object
window = Tk()
window.title("GUI programs using python!")
window.minsize(width=500, height=300)
window["bg"] = "#1e1f22"

elements_to_pack = []

# create a label component
my_label = Label(text="This is a label widget", font=("Arial", 14,"normal"))
elements_to_pack.append(my_label)
# specify layout of the component
my_label["text"] = "Changed the label text"

# text input field
my_input = Entry()
elements_to_pack.append(my_input)

def button_click_label():
    # get the input from entry and set as label text
    my_label.config(text=my_input.get())

my_button_1 = Button(text="Click To Update", command=button_click_label)
elements_to_pack.append(my_button_1)

# text input filed
my_text = Text(height=5, width=30)
elements_to_pack.append(my_text)

def button_click_text():
    my_label.config(text= my_text.get("1.0", END))

my_button_2 = Button(text="CLick To Update", command=button_click_text)
elements_to_pack.append(my_button_2)

def spinbox_value():
    my_label["text"] = spinbox.get()

spinbox = Spinbox(from_=1, to=5, command=spinbox_value, width=5)
elements_to_pack.append(spinbox)

def scale_update(value):
    my_label["text"] = value

scale = Scale(from_=6, to=10, command=scale_update)
elements_to_pack.append(scale)

def checkbutton_update():
    # 1 if On button checked, otherwise 0
    my_label["text"] = checkbutton_state.get()

#variable to hold on to checked state, 0 is off, 1 is on
checkbutton_state = IntVar()
checkbutton = Checkbutton(text="Is this selected?", command=checkbutton_update, variable=checkbutton_state)
elements_to_pack.append(checkbutton)

def radio_option_selected():
    my_label.config(text=radio_state.get())

#Variable to hold on to which radio button value is checked
radio_state = IntVar()
radiobutton1 = Radiobutton(text="Option 1", value="1", variable=radio_state, command=radio_option_selected)
elements_to_pack.append(radiobutton1)
radiobutton2 = Radiobutton(text="Option 2", value="2", variable=radio_state, command=radio_option_selected)
elements_to_pack.append(radiobutton2)

def listbox_option(event):
    # print(listbox.get(listbox.curselection()))
    my_label["text"] = listbox.get(listbox.curselection())

listbox = Listbox()
elements_to_pack.append(listbox)
cars = ["BMW", "Nissan", "Corvette", "Jaguar", "Land Rover"]

for car in cars:
    listbox.insert(cars.index(car), car)

listbox.bind("<<ListboxSelect>>", listbox_option)

# my_label.pack()
# my_button_1.pack()
# my_input.pack()
# my_text.pack()
# my_button_2.pack()
# spinbox.pack()
# scale.pack()
# checkbutton.pack()

for element in elements_to_pack:
    element.pack()

window.mainloop()