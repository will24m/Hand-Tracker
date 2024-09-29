import sys
import os
import threading
from tkinter import Tk

# Add the parent directory of the current file to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import hand_tracker  # Now Python should be able to find hand_tracker.py

class HandTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Tracker - Live Feed")

        # Open the hand tracking window in a new thread
        self.thread = threading.Thread(target=hand_tracker.run_tracker_window)
        self.thread.start()

        # Ensure proper closure when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def exit_app(self):
        """Close the application safely."""
        if self.thread and self.thread.is_alive():
            self.thread.join()  # Wait for the thread to stop
        self.root.quit()  # Close the tkinter app

if __name__ == "__main__":
    root = Tk()
    app = HandTrackerApp(root)
    root.mainloop()
