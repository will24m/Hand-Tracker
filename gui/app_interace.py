import tkinter as tk
import cv2
from hand_tracker import run_tracker
import threading

class HandTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Tracker GUI")
        self.is_running = False
        self.cap = None  # To hold the video capture object
        self.thread = None

        # Start/Stop Button
        self.start_button = tk.Button(root, text="Start Hand Tracker", command=self.start_tracking)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Hand Tracker", state="disabled", command=self.stop_tracking)
        self.stop_button.pack(pady=10)

        # Exit Button
        self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
        self.exit_button.pack(pady=10)

    def start_tracking(self):
        """Start the hand tracking in a separate thread."""
        self.is_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        # Start hand tracking in a new thread to avoid freezing the GUI
        self.thread = threading.Thread(target=self.run_hand_tracker)
        self.thread.start()

    def stop_tracking(self):
        """Stop the hand tracking."""
        self.is_running = False
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
        self.is_running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()  # Ensure the thread is stopped

        self.root.quit()  # Close the tkinter app

if __name__ == "__main__":
    root = tk.Tk()
    app = HandTrackerApp(root)
    root.mainloop()
