import cv2
from PIL import Image, ImageTk
import tkinter as tk

class HandTrackerWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Tracker - Live Feed")
        self.stop_button = None
        self.video_label = None
        self.stop_tracking = False

        # Open the default camera
        self.cap = cv2.VideoCapture(0)

        # Check if the camera is opened successfully
        if not self.cap.isOpened():
            print("Error: Could not open video device.")
            self.cap.release()
            return

        # Set video frame width and height (Optional)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Create the UI elements
        self.create_widgets()

        # Start the video update loop
        self.update_video()

    def create_widgets(self):
        """Create the video display and stop button."""
        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        self.stop_button = tk.Button(self.root, text="Stop Tracking", command=self.stop_tracking_func, 
                                     height=2, width=20, bg="red", font=("Helvetica", 12))
        self.stop_button.pack(pady=10)

    def update_video(self):
        """Update the video stream inside the Tkinter window."""
        if not self.stop_tracking:
            ret, frame = self.cap.read()
            if ret:
                try:
                    # Flip and process the frame
                    frame = cv2.flip(frame, 1)
                    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Convert the OpenCV image to PIL image
                    img = Image.fromarray(img)

                    # Create the ImageTk object to be used in Tkinter
                    imgtk = ImageTk.PhotoImage(image=img)

                    # Safely update the video_label with the new frame
                    self.video_label.imgtk = imgtk  # Keep a reference to avoid garbage collection
                    self.video_label.configure(image=imgtk)

                except Exception as e:
                    print(f"Error updating image: {e}")
            else:
                print("Error: Could not read frame from video stream.")
            
            # Schedule the next frame update in the main thread using root.after()
            self.root.after(10, self.update_video)
        else:
            # Release the camera and close the window when stopped
            self.cap.release()
            cv2.destroyAllWindows()
            self.root.quit()

    def stop_tracking_func(self):
        """Function to stop tracking and close the window."""
        self.stop_tracking = True


def run_tracker_window():
    """Run the hand tracker in a Tkinter window."""
    root = tk.Tk()
    app = HandTrackerWindow(root)
    root.mainloop()
