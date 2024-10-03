# First, we need to load some special tools or libraries that help us work with images and videos.
# Think of these libraries like extra tools in a toolbox that can do specific jobs really well.
# We are using 'cv2', which is part of OpenCV, a library that helps us work with live video from a camera.
import cv2

# We are also using a function called 'process_frame' from another file (hand_recognition.py).
# This function helps us analyze the video and figure out where the hand is and what it’s doing.
from utils.hand_recognition import process_frame

# Now we define a function called 'run_tracker'. A function is like a recipe or a set of instructions for the computer to follow.
# This function's job is to turn on your camera, process the video to detect hands, and show the result on the screen.
def run_tracker():
    # First, we need to tell the computer to start using the camera. 
    # We use 'cv2.VideoCapture(0)' to start capturing video from the default camera (usually the webcam).
    # The '0' tells the computer to use the default or built-in camera. 
    cap = cv2.VideoCapture(0)  # 'cap' is short for 'capture'. This variable will be used to interact with the camera.

    # Next, we need to check if the camera was successfully turned on.
    # Sometimes, there could be a problem with the camera (maybe it's not connected or there’s an error).
    # So we ask the computer to check if the camera is working with 'cap.isOpened()'.
    if not cap.isOpened():  # If the camera isn't working, this part will run.
        # If the camera doesn't work, we want to print a message telling the user something went wrong.
        print("Error: Could not open video capture.")  # This prints a helpful message to the screen if there's an error.
        # Since the camera isn't working, we will stop running the rest of the function.
        return  # 'return' stops the function from doing anything else if there's an error.

    # Now we enter a loop, which means we will do the same steps over and over again until we decide to stop.
    # In this case, the loop will keep capturing video frames (like a series of pictures) from the camera.
    # Each frame will be processed one by one to detect a hand, and the result will be shown on the screen.
    while True:
        # 'cap.read()' is used to capture a single frame from the video.
        # The frame is like a picture that we process and display.
        # 'ret' is a boolean (True or False) that tells us if the frame was captured successfully.
        # 'frame' is the actual image that we will work with.
        ret, frame = cap.read()  # This line captures one frame from the video feed.

        # We need to check if the frame was successfully captured.
        # If not, that means something went wrong while getting the video from the camera.
        # So if 'ret' is False, it means we failed to capture the frame.
        if not ret:
            # If we couldn't capture the frame, we print a message to let the user know.
            print("Failed to capture frame")  # This message will appear if there was a problem.
            break  # 'break' stops the loop, meaning we won't keep trying to capture more frames if there's a problem.

        # Now we need to process the frame we just captured.
        # This is where the magic happens! We send the frame (the image) to the 'process_frame' function,
        # which analyzes the image to detect hands and find out if they are open, closed, or how many fingers are raised.
        # The function returns two things: 
        # - The processed 'frame' (image) with any drawings on it, like the hand landmarks or connections.
        # - The 'status', which is a message describing what the hand is doing (e.g., "Hand Open", "Fingers Raised: 2").
        frame, status = process_frame(frame)  # 'process_frame' does all the hard work of figuring out what's in the frame.

        # We want to show the user what the hand is doing in real-time.
        # So we will write the 'status' (the message about what the hand is doing) on top of the video frame.
        # To do this, we use 'cv2.putText()', which allows us to add text to the image.
        # Here’s what each part does:
        # - 'frame': The image where we want to write the text.
        # - 'status': The message we want to display (like "Hand Open" or "Fingers Raised: 3").
        # - (10, 30): The position (x, y) where the text will appear. This is in pixels, with (10, 30) being near the top-left.
        # - 'cv2.FONT_HERSHEY_SIMPLEX': This is the font style for the text. It's just a simple font.
        # - 1: The size of the text.
        # - (0, 255, 0): This is the color of the text, using BGR format (blue, green, red). (0, 255, 0) is green.
        # - 2: The thickness of the text.
        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  # This writes the status on the video frame.

        # Now we need to show the user the video feed with the hand tracking information.
        # 'cv2.imshow()' opens a window to display the image. The window will be called "Hand Tracker".
        # The 'frame' is the image that will be shown in the window.
        cv2.imshow("Hand Tracker", frame)  # This line shows the live video with hand tracking in a window.

        # We need to give the user a way to stop the program.
        # Here, we are waiting for the user to press a key on the keyboard.
        # 'cv2.waitKey(1)' waits for a key press, and we check if the 'q' key was pressed.
        # If the user presses 'q', we break out of the loop and stop capturing video.
        # '& 0xFF' is a bitwise operation to ensure compatibility with different systems.
        if cv2.waitKey(1) & 0xFF == ord('q'):  # If the user presses 'q', this will trigger.
            break  # 'break' means we will exit the loop and stop the program.

    # Once the loop is done (because the user pressed 'q'), we need to clean up.
    # First, we release the video capture object. This tells the camera to stop recording video.
    cap.release()  # This stops the camera from capturing video.

    # Then we close any windows that were opened by OpenCV (like the "Hand Tracker" window).
    # 'cv2.destroyAllWindows()' closes all the windows that were opened during the program.
    cv2.destroyAllWindows()  # This closes any OpenCV windows that are open.

# The last part of the code is a safety check.
# It ensures that this script is being run directly (not imported into another program).
# If this script is being run directly, it will call the 'run_tracker()' function to start the hand tracking.
if __name__ == "__main__":
    run_tracker()  # This starts the hand tracker if the script is run directly.
