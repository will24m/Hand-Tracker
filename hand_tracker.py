import cv2
import time
import os
from utils.hand_recognition import process_frame
from utils.logging import log_event

# OpenCV Video Capture
cap = cv2.VideoCapture(0)

# Create logs and snapshots directories if they don't exist
if not os.path.exists("logs"):
    os.makedirs("logs")
if not os.path.exists("snapshots"):
    os.makedirs("snapshots")

# Initialize the hand open/close counter and the start time
hand_open_count = 0
hand_close_count = 0
last_status = None
start_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and process the frame to detect hands, gestures, and raised fingers
    frame = cv2.flip(frame, 1)
    processed_frame, status = process_frame(frame)

    # Update hand open/close counters based on gesture detection
    if "Hand Open" in status and last_status != "Hand Open":
        hand_open_count += 1
        log_event("Hand Open")  # Log hand open event
        # Save snapshot when hand opens
        snapshot_filename = f"snapshots/hand_open_{hand_open_count}.jpg"
        cv2.imwrite(snapshot_filename, frame)
    elif "Hand Closed" in status and last_status != "Hand Closed":
        hand_close_count += 1
        log_event("Hand Closed")  # Log hand closed event
    last_status = "Hand Open" if "Hand Open" in status else "Hand Closed"

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

    # Display counters and status
    cv2.putText(processed_frame, status, (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(processed_frame, f'Opens: {hand_open_count}', (50, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(processed_frame, f'Closes: {hand_close_count}', (50, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(processed_frame, f'Time: {elapsed_time_str}', (50, 250),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Show the frame
    cv2.imshow('Hand Tracker', processed_frame)

    # Exit on 'q' key press
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
