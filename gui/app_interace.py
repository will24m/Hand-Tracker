import tkinter as tk
from hand_tracker import run_tracker

class HandTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Tracker GUI")
        self.is_running = False

        # Start/Stop Button
        self.start_button = tk.Button(root, text="Start Hand Tracker", command=self.start_tracking)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Hand Tracker", state="disabled", command=self.stop_tracking)
        self.stop_button.pack(pady=10)

    def start_tracking(self):
        self.is_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        run_tracker()  # Starts the hand tracker from hand_tracker.py

    def stop_tracking(self):
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        # Add logic to stop the camera capture (can be done via a flag in hand_tracker.py)

if __name__ == "__main__":
    root = tk.Tk()
    app = HandTrackerApp(root)
    root.mainloop()
