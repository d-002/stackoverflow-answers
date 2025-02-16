# real-time-tkinter-gui

> [!NOTE]\
> This is not a finished project, but I don't even think I will ever finish it, as I explained it in several comments on [this page](https://stackoverflow.com/questions/71546744).
> 
> This code may not even work properly in some edge cases, and the whole purpose of it is basically to show that this approach is stupidly complicated (at least for me) for what it achieves compared to the other alternatives and completely not worth it.

Context: [Faraaz Kurawle](https://stackoverflow.com/users/16187613) wanted a live update of a Python code that used [tkinter](https://docs.python.org/3/library/tkinter.html).

### Quotes from comments that I hope explain my opinion better:

> The problem with your request is that we not only need to reflect the changes to the GUI, but also to the normal code itself.
> What you want is finally just a real-time python compiler, and that is already kind of hard by itself, not even counting the part where you need to only update the parts of the code that changed.
> I have been working on it for I would say 10 hours and I am starting to realize that this is really a complicated and complex thing...

> With the code above on GitHub, I still have the problem that when you modify a line with a certain variable in it, deleting it is not enough, you also need to know every impact this line had, and this can range from `global foo` \[*changing what a certain variable name in a function refers to*\] to redefining a variable to something else: the program needs to read the whole code again, and this has basically the same effect as refreshing your page.
> Maybe my solution can help once it's done properly, but only to a certain extend. If you want to go further than that, you will need to either make a new `tkinter`-like library, or rewrite the entire Python language

I am sorry for not putting more effort into this, but as I repeated above, it is certainly not worth it. But surely someone can prove me wrong and make this code work?
