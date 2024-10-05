# Importing necessary libraries for working with video and image processing.
import cv2  # OpenCV library helps us work with video streams and images.
from utils.hand_recognition import process_frame  # Custom function to analyze each frame and detect hand gestures.

# Function that starts the hand tracker.
def run_tracker():
    # Start capturing video from the default camera (0 refers to the default camera, usually the webcam).
    # The 'cap' object will be used to interact with the camera.
    cap = cv2.VideoCapture(0)  # VideoCapture(0) opens the default camera.

    # Check if the camera was successfully opened. If not, display an error message and exit the function.
    if not cap.isOpened():  # If the camera couldn't be accessed...
        print("Error: Could not open video capture.")  # Let the user know there's an issue with the camera.
        return  # Exit the function as there's no point in continuing without the camera.

    # Display a message that the video stream has started.
    print("Video stream started. Press 'q' to exit.")

    # We enter a loop to continuously capture and process each video frame until the user decides to stop.
    # This loop will run indefinitely until broken by the user pressing 'q'.
    while True:
        # Capture a single frame from the video stream.
        ret, frame = cap.read()  # 'ret' is a boolean (True/False) indicating if the capture was successful, 'frame' is the image captured.

        # If the frame couldn't be captured for some reason, print an error message and break the loop.
        if not ret:  # If 'ret' is False, something went wrong with capturing the video frame.
            print("Failed to capture frame")  # Let the user know something went wrong.
            break  # Exit the loop.

        # Process the captured frame using the hand recognition function to detect hands and gestures.
        # The 'process_frame' function returns two values:
        # - A processed frame with annotations (like hand landmarks) drawn on it.
        # - A status message (e.g., "Hand Open" or "Fingers Raised: 3") describing what the hand is doing.
        frame, status = process_frame(frame)  # Process the frame for hand detection and get the status.

        # Add the status message (e.g., "Hand Open") to the frame, so the user can see it in real-time.
        # We're placing the message at position (10, 30) on the video feed using green text.
        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  # Write the status message on the frame.

        # Show the frame in a window called "Hand Tracker". This will display the live video feed with the hand status.
        cv2.imshow("Hand Tracker", frame)  # Display the frame with the hand tracking information.

        # Check if the user pressed the 'q' key to exit the program.
        # 'cv2.waitKey(1)' waits for 1 millisecond and checks if a key is pressed.
        # If the 'q' key is pressed, we break out of the loop and stop the program.
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Check if 'q' was pressed.
            print("Exiting hand tracker...")  # Print a message indicating the tracker is closing.
            break  # Exit the loop.

    # After the loop ends, we need to clean up.
    # Release the video capture object (tell the camera to stop recording).
    cap.release()  # Stop capturing video.

    # Close any OpenCV windows that were opened during the program (like the "Hand Tracker" window).
    cv2.destroyAllWindows()  # Close all OpenCV windows.

# The final part of the script ensures that this function only runs if the script is executed directly (not imported).
# If this script is run directly, the 'run_tracker()' function will be called to start the hand tracker.
if __name__ == "__main__":
    run_tracker()  # Start the hand tracker if the script is being run directly.
