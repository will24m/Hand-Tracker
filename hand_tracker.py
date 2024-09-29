import cv2
import time
import os
from PIL import Image, ImageTk
import tkinter as tk

# Flag to control when to stop the video stream
stop_tracking = False

class HandTrackerWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Tracker - Live Feed")
        self.stop_button = None
        self.video_label = None
        self.stop_tracking = False
        self.hand_open_count = 0
        self.hand_close_count = 0
        self.last_status = None
        self.start_time = time.time()
        self.cap = cv2.VideoCapture(0)

        # Create the UI elements
        self.create_widgets()

        # Start the video update loop
        self.update_video()

    def create_widgets(self):
        """Create the video display and stop button."""
        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        self.stop_button = tk.Button(self.root, text="Stop Tracking", command=self.stop_tracking_func, height=2, width=20, bg="red", font=("Helvetica", 12))
        self.stop_button.pack(pady=10)

    def update_video(self):
        """Update the video stream inside the Tkinter window."""
        if not self.stop_tracking:
            ret, frame = self.cap.read()
            if not ret:
                return

            # Flip and process the frame
            frame = cv2.flip(frame, 1)
            processed_frame, status = self.process_frame(frame)

            # Convert frame to PIL image format to display in Tkinter
            img = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)

            # Update the label with the new frame
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

            # Continue updating after 10 ms
            self.root.after(10, self.update_video)
        else:
            # Release the camera and close the window when stopped
            self.cap.release()
            cv2.destroyAllWindows()
            self.root.quit()

    def process_frame(self, frame):
        """Process the frame and track hand gestures and raised fingers."""
        status = "No Hand Detected"
        # (Insert your existing logic for hand gesture detection here)
        # For now, we'll simulate by showing dummy status
        status = f"Dummy Status: Hand Open/Closed, Fingers Raised: {0}"

        # Display some dummy information for hand open/close counting
        cv2.putText(frame, f'Opens: {self.hand_open_count}', (50, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Closes: {self.hand_close_count}', (50, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        elapsed_time = time.time() - self.start_time
        elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        cv2.putText(frame, f'Time: {elapsed_time_str}', (50, 250),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        return frame, status

    def stop_tracking_func(self):
        """Function to stop tracking and close the window."""
        self.stop_tracking = True


def run_tracker_window():
    """Run the hand tracker in a Tkinter window."""
    root = tk.Tk()
    app = HandTrackerWindow(root)
    root.mainloop()

