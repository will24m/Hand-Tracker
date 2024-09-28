import cv2
from utils.hand_recognition import process_frame

# OpenCV Video Capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and process the frame to detect hands and gesture
    frame = cv2.flip(frame, 1)
    processed_frame = process_frame(frame)

    # Display the frame with annotations
    cv2.imshow('Hand Tracker', processed_frame)

    # Exit on 'q' key press
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
