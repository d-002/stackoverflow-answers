from tkinter import *

with open('data.txt') as f:
    data = f.read()

tk = Tk()
Label(tk, text=data).pack()
tk.mainloop()
