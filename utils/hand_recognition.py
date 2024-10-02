import cv2
import mediapipe as mp
import numpy as np
import math
import torch
import matplotlib.pyplot as plt
from collections import deque
import winsound  # for sound alerts on gestures (optional)

# Initialize MediaPipe components
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Gesture history and counters
gesture_history = deque(maxlen=100)
gesture_count = {"Hand Open": 0, "Fist Closed": 0, "Partially Open Hand": 0}

# Initialize PyTorch model (simple fully connected network for classification)
class GestureNet(torch.nn.Module):
    def __init__(self):
        super(GestureNet, self).__init__()
        self.fc1 = torch.nn.Linear(21 * 3, 128)  # 21 landmarks, each with (x, y, z) coordinates
        self.fc2 = torch.nn.Linear(128, 3)  # Output: 3 classes (open hand, fist, partial)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return torch.softmax(x, dim=1)

model = GestureNet()

# Placeholder for real-time classification output
gesture_probabilities = {"Hand Open": 0.0, "Fist Closed": 0.0, "Partially Open Hand": 0.0}

# Helper function to calculate Euclidean distance
def calculate_distance(point1, point2):
    return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

def process_frame(frame):
    global gesture_probabilities
    with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        status = "No Hand Detected"
        num_fingers_raised = 0
        hand_landmarks_array = []

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                open_status = classify_hand_gesture(hand_landmarks)
                num_fingers_raised = count_raised_fingers(hand_landmarks)

                # Prepare the hand landmarks data for gesture classification
                hand_landmarks_array = [landmarks_to_array(hand_landmarks)]

                # Update gesture count and history
                gesture_history.append(open_status)
                gesture_count[open_status] += 1

                # Update status
                status = f"{open_status}, Fingers Raised: {num_fingers_raised}"

                # Play sound if fist is closed (optional)
                if open_status == "Fist Closed":
                    winsound.Beep(1000, 200)

        # Gesture classification using PyTorch model
        if hand_landmarks_array:
            prediction = model(torch.Tensor(hand_landmarks_array))
            gesture_probabilities = {
                "Hand Open": prediction[0, 0].item(),
                "Fist Closed": prediction[0, 1].item(),
                "Partially Open Hand": prediction[0, 2].item(),
            }

        return frame, status

def classify_hand_gesture(landmarks):
    palm_center = landmarks.landmark[mp_hands.HandLandmark.WRIST]
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    
    thumb_distance = calculate_distance(thumb_tip, palm_center)
    thumb_folded = thumb_distance < calculate_distance(thumb_ip, palm_center)

    finger_tips = [landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                   landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                   landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                   landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]]

    finger_knuckles = [landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP],
                       landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP],
                       landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP],
                       landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]]

    open_fingers = sum(1 for tip, knuckle in zip(finger_tips, finger_knuckles) if tip.y < knuckle.y)
    
    if not thumb_folded:
        open_fingers += 1

    if open_fingers == 0:
        return "Fist Closed"
    elif open_fingers >= 3:
        return "Hand Open"
    else:
        return "Partially Open Hand"

def count_raised_fingers(landmarks):
    finger_tips = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]

    finger_knuckles = [
        mp_hands.HandLandmark.THUMB_IP,
        mp_hands.HandLandmark.INDEX_FINGER_MCP,
        mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
        mp_hands.HandLandmark.RING_FINGER_MCP,
        mp_hands.HandLandmark.PINKY_MCP
    ]

    raised_fingers = 0
    for tip, knuckle in zip(finger_tips, finger_knuckles):
        if landmarks.landmark[tip].y < landmarks.landmark[knuckle].y and abs(landmarks.landmark[tip].x - landmarks.landmark[knuckle].x) < 0.1:
            raised_fingers += 1

    return raised_fingers

def landmarks_to_array(landmarks):
    """Convert hand landmarks to a flat array for ML model input."""
    return [coord for landmark in landmarks.landmark for coord in (landmark.x, landmark.y, landmark.z)]

def plot_gesture_stats():
    """Plot real-time gesture statistics using Matplotlib."""
    plt.ion()  # Interactive mode on
    fig, ax = plt.subplots()
    while True:
        ax.clear()
        ax.bar(gesture_count.keys(), gesture_count.values())
        plt.draw()
        plt.pause(0.1)
