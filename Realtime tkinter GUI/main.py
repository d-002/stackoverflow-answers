import os
import time
import difflib # to compare before and after changes have been made to the file
from os.path import *
from threading import Thread
from tkinter import Tk
from tkinter.messagebox import showerror

# this part is for duplicated lines hendling

# removes duplicates and keeps the order
def set_list(l):
    new_list = []
    for element in l:
        if element not in new_list:
            new_list.append(element)

    return new_list

# checks if the following slice of string is a complete line (not part of it)
def slice_is_a_line(string, start, end):
    ok = [False, False]
    if start:
        ok[0] = string[start] == '\t' or string[start-1] == '\t'
    else:
        ok[0] = True
    if end < len(string)-1:
        ok[1] = string[end] == '\t' or string[end-1] == '\t'
    else:
        ok[1] = True
    return sum(ok) == 2

# lines which contain at least a part of the specified slice
def lines_that_touch(string, start, end):
    n_linebreaks = string.count('\t', 0, start)
    index = start
    yield n_linebreaks
    for index in range(start, end):
        if string[index] == '\t':
            n_linebreaks += 1
            yield n_linebreaks

# same, but without the first and last one
def lines_that_touch_inner(string, start, end):
    n_linebreaks = string.count('\t', 0, start+1)
    index = start
    yield n_linebreaks
    for index in range(start, end):
        if string[index] == '\t' and index < end-1:
            n_linebreaks += 1
            yield n_linebreaks

# what has been removed ot added since last time? (only work in lines, not words or whatever small thing
def what_removed_added(before, after):
    before_lines = before
    after_lines = after
    before = after = '' # need to be concatenated
    for line in before_lines:
        before += line + '\t' # I suppose you will not use this character much
    before = before[:-1]
    for line in after_lines:
        after += line + '\t'
    after = after[:-1]

    seq_mat = difflib.SequenceMatcher(a=before, b=after, autojunk=True)

    removed = []
    added = []

    for operation, i1,i2,j1,j2 in seq_mat.get_opcodes():
        if operation == 'delete':
            if slice_is_a_line(before, i1, i2):
                for line in lines_that_touch_inner(before, i1, i2):
                    added.append(before_lines[line])
            else:
                for line in lines_that_touch(before, i1, i2):
                    removed.append(before_lines[line])
                for line in lines_that_touch(after, j1, j2):
                    added.append(after_lines[line])
        elif operation == 'replace':
            removed.append(before_lines[before.count('\t', 0, i2)])
            added.append(after_lines[after.count('\t', 0, j2)])
        elif operation == 'insert':
            if slice_is_a_line(after, j1, j2):
                for line in lines_that_touch_inner(after, j1, j2):
                    added.append(after_lines[line])
            else:
                for line in lines_that_touch(before, i1, i2):
                    removed.append(before_lines[line])
                for line in lines_that_touch(after, j1, j2):
                    added.append(after_lines[line])

    return set_list(removed), set_list(added)

# this part is the main one

class CheckableTk(Tk):
    def __init__(self, *args, **kwargs):
        self.running = False
        super().__init__(*args, **kwargs)

    def mainloop(self, *args, **kwargs):
        self.running = True
        try:
            return super().mainloop(*args, **kwargs)
        finally:
            self.running = False

def spaces_at_start(string):
    n = 0
    for char in string:
        if char == ' ':
            n += 1
        else:
            return n//indent_size
    return n

def display_file():
    global prev_lines, added_vars_per_line

    empty_line = lambda string: list(set(string)) == [' '] or not len(string)

    with open(tk_filename) as f:
        # uses the class above to check if mainloop if running
        lines_raw = f.read().replace('Tk', 'CheckableTk').split('\n')

    lines = []
    waiting_for_unindent = False
    current_line = ''

    # group lines forming for example functions
    for y_position in range(len(lines_raw)):
        if empty_line(lines_raw[y_position]):
            continue

        indent0 = spaces_at_start(lines_raw[y_position])
        if y_position < len(lines_raw)-1:
            indent1 = spaces_at_start(lines_raw[y_position+1])
        else:
            indent1 = indent0 # end of file, no indentation difference

        if indent0 < indent1: # indent
            waiting_for_unindent += 1
        elif indent0 > indent1: # unindent
            waiting_for_unindent -= 1

        if waiting_for_unindent:
            current_line += lines_raw[y_position]+'\n'
        else:
            current_line += lines_raw[y_position]
            lines.append(current_line)
            current_line = ''

    removed, added = what_removed_added(prev_lines, lines)
    print(removed)
    print(added)

    remove_add(lines, remove, add)

    added_vars_per_line = added_vars_per_line_
    prev_lines = lines
    print('\nDone.\n')

# remove lines that no longer exist, and add lines that were created
def remove_add(lines, remove, add):
    index = 0
    added_vars_per_line_ = [[]]*len(lines)
    for line in lines: # need to index through everything to know how many lines have passed
        if empty_line(line):
            continue

        # if a line changed, or has been added to the file, update
        if line in added:
            print('Adding line:')
            print(' ', line)
            try:
                globals_before = dict(globals())
                exec(line, globals()) # store the eventual variables in globals()
                added_vars = [globals()[var] for var in globals() if var not in globals_before.keys()]

                for var in added_vars:
                    if type(var) == CheckableTk: # new GUI
                        GUIs.append(var)
                for GUI in GUIs: # update all of them
                    GUI.update()

                added_vars_per_line_[index] = added_vars
            except Exception as e:
                error_win = Tk()
                error_win.wm_attributes('-alpha', 0) # transparent
                showerror(str(type(e)), 'Line %d:\n%s' %(index+1, e))
                error_win.destroy()

                # don't draw the rest after the error showed up
                added_vars_per_line = added_vars_per_line_
                return

        # if a line has been removed (or also changed), update
        if line in removed:
            print('Removing line:')
            print(' ', line)
            # delete all created variables
            print(added_vars_per_line)
            for var in added_vars_per_line[index]:
                for GUI in GUIs:
                    try:
                        var.destroy()
                    except: # the var was not a widget or did not belong to this GUI
                        pass
                exec('del %s' %var, globals())

        index += 1

def check_need_update():
    global need_update # used to send order to the main thread
    prev_size = 0

    while True:
        # Getting the size of the file for comparison.
        size = getsize(tk_filename)
        if size != prev_size:
            # stop all mainloop() to allow the main thread to compile once again
            for GUI in GUIs:
                if GUI.running:
                    GUI.quit()
                    GUI.running = 0.5
                    # will be launched again after compiling the code
                    print('\nGUI quit')
            while need_update: # wait for the main thread to process and set the variable to False
                time.sleep(0.1)
            print('\nrequesting update')
            need_update = True
        prev_size = size

        # wait a bit, no need to use all the computer power just to redraw a window
        time.sleep(1)

tk_filename = 'file to display.py'
need_update = False
prev_lines = []
GUIs = []
added_vars_per_line = []

indent_size = 4 # python standard

Thread(target=check_need_update).start()
while True:
    if need_update:
        print('starting update')
        display_file()
        print('end of update')
        for GUI in GUIs:
            if GUI.running == 0.5: # launch the previously launched GUIs again
                print('restarting GUI')
                GUI.mainloop()
        need_update = False
