import sys
import os

# Add the parent directory of gui to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
import cv2
from hand_tracker import run_tracker  # Assuming this exists
import threading

class HandTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Tracker GUI")
        self.is_running = False
        self.cap = None  # To hold the video capture object
        self.thread = None

        # Configure the window size
        self.root.geometry("400x300")

        # Start Button
        self.start_button = tk.Button(root, text="Start Hand Tracker", command=self.start_tracking, 
                                      height=2, width=20, bg="lightgreen", font=("Helvetica", 12))
        self.start_button.pack(pady=20)

        # Stop Button (big and at the bottom)
        self.stop_button = tk.Button(root, text="Stop Hand Tracker", state="disabled", command=self.stop_tracking, 
                                     height=2, width=20, bg="red", font=("Helvetica", 12))
        self.stop_button.pack(side="bottom", pady=20)

        # Exit Button (at the bottom)
        self.exit_button = tk.Button(root, text="Exit", command=self.exit_app, 
                                     height=2, width=20, bg="lightblue", font=("Helvetica", 12))
        self.exit_button.pack(side="bottom", pady=10)

        # Ensure proper closure when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def start_tracking(self):
        """Start the hand tracking in a separate thread."""
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            
            # Start hand tracking in a new thread to avoid freezing the GUI
            self.thread = threading.Thread(target=self.run_hand_tracker)
            self.thread.start()

    def stop_tracking(self):
        """Stop the hand tracking."""
        if self.is_running:
            self.is_running = False
            if self.thread:
                self.thread.join()  # Wait for the thread to stop
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")

    def run_hand_tracker(self):
        """Run hand tracking logic."""
        cap = cv2.VideoCapture(0)
        while self.is_running:
            ret, frame = cap.read()
            if not ret:
                break

            # Hand tracking and frame processing
            frame = cv2.flip(frame, 1)
            cv2.imshow("Hand Tracker", frame)

            # Exit on 'q' key press
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def exit_app(self):
        """Close the application safely."""
        if self.is_running:
            self.stop_tracking()  # Ensure tracking is stopped before closing
        self.root.quit()  # Close the tkinter app


if __name__ == "__main__":
    root = tk.Tk()
    app = HandTrackerApp(root)
    root.mainloop()
