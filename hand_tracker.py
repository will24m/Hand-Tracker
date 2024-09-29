import cv2
import mediapipe as mp
from PIL import Image, ImageTk
import tkinter as tk

class HandTrackerWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Tracker - Live Feed")
        self.stop_tracking = False

        # Mediapipe hand detection setup
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.mp_draw = mp.solutions.drawing_utils

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

        # Create the video display label
        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        # Create the counters for palm open/close and fingers raised
        self.open_palm_count = 0
        self.closed_palm_count = 0
        self.fingers_count_label = tk.Label(self.root, text="Fingers up: 0", font=("Helvetica", 16))
        self.fingers_count_label.pack()
        self.palm_state_label = tk.Label(self.root, text="Open palm count: 0, Closed palm count: 0", font=("Helvetica", 16))
        self.palm_state_label.pack()

        # Start the video update loop
        self.update_video()

    def update_video(self):
        """Update the video stream inside the Tkinter window."""
        if not self.stop_tracking:
            ret, frame = self.cap.read()
            if ret:
                try:
                    # Flip and process the frame
                    frame = cv2.flip(frame, 1)
                    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Hand detection and finger counting
                    results = self.hands.process(img)

                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                            # Finger counting logic
                            fingers_up = self.count_fingers(hand_landmarks)
                            self.fingers_count_label.config(text=f"Fingers up: {fingers_up}")

                            # Palm state detection
                            palm_open = self.is_palm_open(hand_landmarks)
                            if palm_open:
                                self.open_palm_count += 1
                            else:
                                self.closed_palm_count += 1

                            self.palm_state_label.config(text=f"Open palm count: {self.open_palm_count}, Closed palm count: {self.closed_palm_count}")

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

    def count_fingers(self, hand_landmarks):
        """Count how many fingers are raised."""
        fingers_up = 0

        # Thumb: compare landmark 4 and 2
        if hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP].x:
            fingers_up += 1

        # Fingers: compare landmark 8 (tip) with landmark 6 (middle)
        for finger in [self.mp_hands.HandLandmark.INDEX_FINGER_TIP, self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                       self.mp_hands.HandLandmark.RING_FINGER_TIP, self.mp_hands.HandLandmark.PINKY_TIP]:
            if hand_landmarks.landmark[finger].y < hand_landmarks.landmark[finger - 2].y:
                fingers_up += 1

        return fingers_up

    def is_palm_open(self, hand_landmarks):
        """Determine if the palm is open or closed based on distance between landmarks."""
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]

        # If thumb and pinky are far apart, the palm is likely open
        distance = abs(thumb_tip.x - pinky_tip.x)
        return distance > 0.25

def run_tracker_window():
    """Run the hand tracker in a Tkinter window."""
    root = tk.Tk()
    app = HandTrackerWindow(root)
    root.mainloop()
