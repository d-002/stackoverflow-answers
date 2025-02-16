from urllib.request import *
from zipfile import ZipFile
from os import chdir, mkdir, remove
from os.path import join, exists

from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo, showerror, showwarning

def browse():
    global path
    path['text'] = askdirectory()

def install():
    if len(path['text']): # check if valid directory
        try:
            realpath = join(path['text'], 'application name')
            if not exists(realpath):
                mkdir(realpath) # create a subfolder with the application name
            chdir(realpath) # move to that directory

            # download the .zip containing all needed files
            data = urlopen('https://d-002.github.io/install-wizard/application.zip').read()
            with open('application.zip', 'wb') as f:
                f.write(data)

            # unzip the file
            zip = ZipFile('application.zip')
            zip.extractall()
            zip.close()

            # remove the temporary zip file
            remove('application.zip')
            showinfo('Done', 'Completed successfully')
        except Exception as e:
            showerror('Error', 'An error occured: %s' %e)
    else:
        showwarning('Error', 'Please enter a valid path')

def make_gui():
    global tk, path
    tk = Tk()
    Label(tk, text='Path:').grid(row=0, column=0)
    path = Label(tk, text='')
    path.grid(row=0, column=1)
    Button(tk, text='Browse', command=browse).grid(row=0, column=2)
    Button(tk, text='Install', command=install).grid(row=1, column=1, columnspan=3, sticky='ew')

make_gui()
tk.mainloop()
