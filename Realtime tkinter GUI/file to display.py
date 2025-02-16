from random import choice
from tkinter import *

win = Tk()

colors = ['#000', '#f00', '#0f0', '#00f', '#880', '#808', '#088', '#fff']

def clickme():
    colors_ = colors[:]
    colors_.remove(label['fg'])
    label['fg'] = choice(colors_)

btn = Button(win, text='This is a button', width=20, command=clickme)
btn.grid(pady=(10, 0))
label = Label(win, text='Click the button to change my color', fg='#000')
label.grid(padx=10, pady=10)

win.mainloop()
