import sys
import os
import threading
from tkinter import Tk, Button

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hand_tracker import run_tracker_window  # Correct import

class HandTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Tracker GUI")
        self.is_running = False

        # Configure the window size
        self.root.geometry("400x300")

        # Start Button
        self.start_button = Button(root, text="Start Hand Tracker", command=self.start_tracking, 
                                   height=2, width=20, bg="lightgreen", font=("Helvetica", 12))
        self.start_button.pack(pady=20)

        # Exit Button (at the bottom)
        self.exit_button = Button(root, text="Exit", command=self.exit_app, 
                                  height=2, width=20, bg="lightblue", font=("Helvetica", 12))
        self.exit_button.pack(side="bottom", pady=20)

        # Ensure proper closure when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def start_tracking(self):
        """Start the hand tracking in a new window."""
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state="disabled")
            
            # Open the hand tracking window
            run_tracker_window()

    def exit_app(self):
        """Close the application safely."""
        self.root.quit()  # Close the tkinter app


if __name__ == "__main__":
    root = Tk()
    app = HandTrackerApp(root)
    root.mainloop()
