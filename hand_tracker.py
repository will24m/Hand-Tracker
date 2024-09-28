import cv2
import time
from utils.hand_recognition import process_frame

# OpenCV Video Capture
cap = cv2.VideoCapture(0)

# Initialize the hand open/close counter and the start time
hand_open_count = 0
hand_close_count = 0
last_status = None
start_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and process the frame to detect hands and gesture
    frame = cv2.flip(frame, 1)
    processed_frame, status = process_frame(frame)

    # Update hand open/close counters
    if status != last_status:
        if status == "Hand Open":
            hand_open_count += 1
        elif status == "Hand Closed":
            hand_close_count += 1
        last_status = status

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

    # Display counters and timer
    cv2.putText(processed_frame, f'Opens: {hand_open_count}', (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(processed_frame, f'Closes: {hand_close_count}', (50, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(processed_frame, f'Time: {elapsed_time_str}', (50, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # Show the frame
    cv2.imshow('Hand Tracker', processed_frame)

    # Exit on 'q' key press
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
