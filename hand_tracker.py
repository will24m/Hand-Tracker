# First, we import the required libraries that allow us to work with video, hand tracking, and other features
import cv2  # OpenCV is a library for real-time computer vision (like working with cameras and videos)
from utils.hand_recognition import process_frame  # We import the function to process each frame from hand_recognition.py

# This function is responsible for running the hand tracking system
def run_tracker():
    # Initialize the video capture using the default camera (camera 0)
    # This will activate your computer's camera to capture video in real-time
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened correctly
    # If the camera couldn't be accessed, an error message will be printed
    if not cap.isOpened():
        print("Error: Could not open video capture.")  # Tells you if the camera isn't working
        return  # Stops the program if there was an error opening the camera

    # The following code will keep running continuously, processing the video from the camera
    while True:
        # Read a frame from the camera
        # The function 'cap.read()' grabs one frame of the video feed. 'ret' tells us if it was successful.
        ret, frame = cap.read()
        
        # If there was an error grabbing a frame, print an error message and try again
        if not ret:
            print("Failed to capture frame")  # Tells you there was an issue getting the video feed
            break  # Exits the loop if there's a failure

        # Process the frame to detect hands and track gestures
        # The 'process_frame' function detects if there's a hand in the frame and what the hand is doing (open/closed, fingers raised, etc.)
        frame, status = process_frame(frame)

        # Display the processed frame in a window
        # 'cv2.putText()' adds text to the video frame (in this case, it shows the current hand status on the screen)
        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # 'cv2.imshow()' displays the current video frame in a window titled "Hand Tracker"
        cv2.imshow("Hand Tracker", frame)

        # Check if the user has pressed the 'q' key
        # 'cv2.waitKey(1)' waits for the user to press a key. If the key is 'q', we break the loop and stop the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # Exits the loop if the 'q' key is pressed

    # Release the video capture object once the program is done
    # This stops the camera feed and releases any resources being used by OpenCV
    cap.release()

    # Destroy all the OpenCV windows
    # This will close any windows that were opened to display the video feed
    cv2.destroyAllWindows()

# The following code ensures that this script can be run directly from the command line
# This part checks if this script is the "main" one being run (and not just an import into another script)
if __name__ == "__main__":
    run_tracker()  # Calls the 'run_tracker()' function to start the hand tracking process
