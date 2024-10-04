# The first step is to import some tools (libraries) that will help our program run.
# Think of these tools like extra gadgets that let the program do specific jobs.

import sys  # 'sys' allows us to interact with the system or environment running this program (like your computer).
import os  # 'os' lets us interact with the operating system, which is the part of your computer that manages files and hardware.
import threading  # 'threading' helps us do multiple things at once, like running two tasks side by side.
from tkinter import Tk  # 'Tkinter' is a library that helps us create windows, buttons, and other GUI (Graphical User Interface) elements.

# Next, we need to add the folder where this file is located to the system path.
# The "system path" is like a list of folders where Python looks for files it needs.
# Here, we are telling Python, "Hey, look in the folder where this file is!"
# This is important because we need to find other files, like 'hand_tracker.py', that work together with this file.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now, we need to import a special file we created called 'hand_tracker.py'.
# This file handles the logic for tracking hands using the camera.
import hand_tracker  # This tells Python, "Load the 'hand_tracker.py' file so we can use its functions."

# The main part of our program will be contained inside a class called 'HandTrackerApp'.
# A class is like a blueprint or template that lets us create objects with specific features or actions.
class HandTrackerApp:
    
    # This part of the class is called the 'initializer' or 'constructor'.
    # It runs automatically when we create a new HandTrackerApp object, setting up the program.
    # 'root' is a special thing we pass to create the main window where everything happens.
    def __init__(self, root):
        # First, we store the root window in the object so we can use it later.
        # The 'root' window is the main window of the program.
        self.root = root

        # Now, we give a title to the window that will show up at the top bar (like how apps have names at the top of the screen).
        self.root.title("Hand Tracker - Live Feed")  # The window will be called "Hand Tracker - Live Feed."

        # Next, we need to run the hand tracking program. 
        # Since hand tracking takes time and needs to happen continuously, we run it in a "thread".
        # A thread is like a side job that can run at the same time as other jobs.
        # This is important because we want the hand tracker to keep running without freezing the rest of the program.
        # Here, we start the hand tracking by calling 'run_tracker_window', which is defined in 'hand_tracker.py'.
        self.thread = threading.Thread(target=hand_tracker.run_tracker_window)  # We create a new thread to run the hand tracker.
        self.thread.start()  # This actually starts the thread, which begins the hand tracking in the background.

        # When you close the window (by clicking the 'X' button), we want the program to stop safely.
        # So we use 'protocol' to make sure when you try to close the window, it runs a special function called 'exit_app'.
        # This ensures everything stops properly when you close the app.
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    # Now we define a special function called 'exit_app'.
    # This function will stop everything and close the program properly.
    def exit_app(self):
        # First, we check if the thread (the hand tracker) is still running.
        # If it's running, we need to stop it first before closing the app.
        if self.thread and self.thread.is_alive():
            self.thread.join()  # 'join' makes sure we wait until the thread finishes its job before continuing.

        # Finally, we close the main window of the app.
        # 'root.quit()' will stop the app and close the window, safely exiting the program.
        self.root.quit()

# This part of the code is a check to see if we are running the program directly.
# If we are running this file as the main program, we want to create the window and start the app.
# If it's being used by another program, this part won't run.
if __name__ == "__main__":
    # First, we need to create the root window. 'Tk()' is used to create this window.
    root = Tk()

    # Now, we create an object of our class 'HandTrackerApp', which will set up and run the hand tracking program.
    # We pass the 'root' window to it so that it knows which window to use for the app.
    app = HandTrackerApp(root)

    # Finally, we need to run the program and open the window.
    # 'root.mainloop()' makes the window stay open until you close it.
    # Without this, the window would open and immediately close.
    root.mainloop()
