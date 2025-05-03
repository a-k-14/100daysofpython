import tkinter

import requests

# get new quote from the API
def get_new_quote():
    """
    Gets a new quote from the api -> https://api.kanye.rest/
    and returns the same
    """
    response = requests.get(url="https://api.kanye.rest/")
    response.raise_for_status()
    return response.json()["quote"]

# updates new quote in the UI
def update_quote():
    new_quote = get_new_quote()
    canvas.itemconfig(canvas_quote, text=new_quote)

window = tkinter.Tk()
window.title("Kanye Says...")
window.config(padx=50, pady=30)


canvas = tkinter.Canvas(width=300, height=414, highlightthickness=0)
bg_image = tkinter.PhotoImage(file="./background.png")
canvas.create_image(300/2, 414/2, image=bg_image)
canvas_quote = canvas.create_text(300/2, 414/2, text=get_new_quote(), font=("roboto", 20, "bold"),fill="white", width=250)
canvas.grid(column=0, row=0)

next_quote_bg = tkinter.PhotoImage(file="./kanye.png")
next_quote = tkinter.Button(image=next_quote_bg, cursor="hand2", command=update_quote)
next_quote.grid(column=0, row=1, pady=(10,0))

exit_button = tkinter.Button(text="Grr... close", cursor="hand2", padx=10, pady = 10, command=window.destroy)
exit_button.grid(column=0, row=2, pady=10)

window.mainloop()