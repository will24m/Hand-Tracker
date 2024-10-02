import cv2  # OpenCV library for real-time computer vision
import mediapipe as mp  # MediaPipe library for hand tracking and gesture recognition
import numpy as np  # Numpy library for efficient numerical operations
import math  # Built-in math library, used for distance calculations
import torch  # PyTorch library for machine learning and deep learning models
import matplotlib.pyplot as plt  # Matplotlib for real-time plotting of statistics
from collections import deque  # Deque for keeping track of a sliding window of gesture history
import winsound  # Library for playing sound alerts (optional, used for gesture alerts)

# Initialize the MediaPipe components for hand tracking
mp_hands = mp.solutions.hands  # This is MediaPipe's solution for detecting hands in video frames
mp_drawing = mp.solutions.drawing_utils  # This helps to draw the hand landmarks on video frames

# This is a sliding window (deque) to store the last 100 gestures recognized
gesture_history = deque(maxlen=100)

# A dictionary to keep track of how many times each gesture has been recognized
gesture_count = {"Hand Open": 0, "Fist Closed": 0, "Partially Open Hand": 0}

# Define a simple machine learning model using PyTorch to classify hand gestures
class GestureNet(torch.nn.Module):
    def __init__(self):
        super(GestureNet, self).__init__()
        # The input layer will have 21 landmarks with 3 coordinates (x, y, z)
        self.fc1 = torch.nn.Linear(21 * 3, 128)
        # The output layer will predict 3 classes: open hand, closed fist, or partially open
        self.fc2 = torch.nn.Linear(128, 3)

    # Define how the data flows through the neural network
    def forward(self, x):
        x = torch.relu(self.fc1(x))  # Apply the ReLU activation function to the first layer
        x = self.fc2(x)  # Final output, no activation for the last layer
        return torch.softmax(x, dim=1)  # Apply softmax to turn outputs into probabilities

# Create an instance of the neural network
model = GestureNet()

# A placeholder dictionary to store the real-time probabilities of each gesture
gesture_probabilities = {"Hand Open": 0.0, "Fist Closed": 0.0, "Partially Open Hand": 0.0}

# This function calculates the distance between two points (using their x and y coordinates)
def calculate_distance(point1, point2):
    return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

# This function processes each frame of the video feed
def process_frame(frame):
    global gesture_probabilities  # Reference the global variable for gesture probabilities

    # The MediaPipe hand tracker is initialized here
    with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        # Convert the video frame from BGR (OpenCV default) to RGB (MediaPipe uses RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame with MediaPipe to detect hand landmarks
        result = hands.process(rgb_frame)

        # Default status and number of raised fingers
        status = "No Hand Detected"
        num_fingers_raised = 0
        hand_landmarks_array = []

        # If MediaPipe detects a hand in the frame, process it
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw the hand landmarks on the frame using OpenCV
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Classify the hand gesture (open, closed, or partially open)
                open_status = classify_hand_gesture(hand_landmarks)
                
                # Count how many fingers are raised
                num_fingers_raised = count_raised_fingers(hand_landmarks)

                # Convert hand landmarks to an array to input to the neural network for classification
                hand_landmarks_array = [landmarks_to_array(hand_landmarks)]

                # Update the history and count of gestures
                gesture_history.append(open_status)
                gesture_count[open_status] += 1

                # Update the status text to show in the video frame
                status = f"{open_status}, Fingers Raised: {num_fingers_raised}"

                # Optional: Play a sound if the hand is closed into a fist
                if open_status == "Fist Closed":
                    winsound.Beep(1000, 200)  # A beep sound

        # Use the PyTorch model to classify the gesture (open hand, fist, or partially open)
        if hand_landmarks_array:
            # Convert the hand landmarks to a PyTorch tensor
            prediction = model(torch.Tensor(hand_landmarks_array))
            # Update the probabilities for each gesture
            gesture_probabilities = {
                "Hand Open": prediction[0, 0].item(),
                "Fist Closed": prediction[0, 1].item(),
                "Partially Open Hand": prediction[0, 2].item(),
            }

        return frame, status  # Return the processed frame and the status

# This function classifies the hand as open, closed, or partially open based on landmark positions
def classify_hand_gesture(landmarks):
    # Find the center of the palm using the wrist landmark
    palm_center = landmarks.landmark[mp_hands.HandLandmark.WRIST]
    # Get the coordinates of the thumb tip and thumb joint (IP joint)
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    
    # Calculate the distance between thumb and palm to check if the thumb is folded or not
    thumb_distance = calculate_distance(thumb_tip, palm_center)
    thumb_folded = thumb_distance < calculate_distance(thumb_ip, palm_center)

    # Check the position of each finger tip compared to its knuckle
    finger_tips = [landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                   landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                   landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                   landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]]

    finger_knuckles = [landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP],
                       landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP],
                       landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP],
                       landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]]

    # Count how many fingers are open (fingertips above knuckles)
    open_fingers = sum(1 for tip, knuckle in zip(finger_tips, finger_knuckles) if tip.y < knuckle.y)

    # If the thumb is not folded, count it as an open finger
    if not thumb_folded:
        open_fingers += 1

    # Determine the gesture based on the number of open fingers
    if open_fingers == 0:
        return "Fist Closed"  # No fingers open = fist closed
    elif open_fingers >= 3:
        return "Hand Open"  # 3 or more fingers open = hand open
    else:
        return "Partially Open Hand"  # 1 or 2 fingers open = partially open

# This function counts how many fingers are raised by comparing each fingertip to its knuckle
def count_raised_fingers(landmarks):
    # Define the landmarks for each finger's tip
    finger_tips = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]

    # Define the landmarks for each finger's knuckle
    finger_knuckles = [
        mp_hands.HandLandmark.THUMB_IP,
        mp_hands.HandLandmark.INDEX_FINGER_MCP,
        mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
        mp_hands.HandLandmark.RING_FINGER_MCP,
        mp_hands.HandLandmark.PINKY_MCP
    ]

    raised_fingers = 0

    # For each finger, check if the tip is above the knuckle, which means the finger is raised
    for tip, knuckle in zip(finger_tips, finger_knuckles):
        if landmarks.landmark[tip].y < landmarks.landmark[knuckle].y and abs(landmarks.landmark[tip].x - landmarks.landmark[knuckle].x) < 0.1:
            raised_fingers += 1

    return raised_fingers

# This function converts the hand landmarks into an array format that can be used by the neural network
def landmarks_to_array(landmarks):
    return [coord for landmark in landmarks.landmark for coord in (landmark.x, landmark.y, landmark.z)]

# This function shows real-time statistics of recognized gestures using Matplotlib
def plot_gesture_stats():
    plt.ion()  # Interactive mode is on, so the plot updates in real-time
    fig, ax = plt.subplots()
    while True:
        ax.clear()  # Clear the previous plot
        ax.bar(gesture_count.keys(), gesture_count.values())  # Create a bar chart with gesture counts
        plt.draw()  # Draw the updated plot
        plt.pause(0.1)  # Pause for 0.1 seconds to allow real-time updating
