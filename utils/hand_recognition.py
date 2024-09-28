import cv2
import mediapipe as mp

# Initialize MediaPipe components
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Hand recognition logic
def process_frame(frame):
    with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame to detect hands
        result = hands.process(rgb_frame)

        status = "No Hand Detected"

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw landmarks and connections
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Classify hand gesture (open or closed)
                status = classify_hand_gesture(hand_landmarks)
                
        return frame, status

def classify_hand_gesture(landmarks):
    # Extract finger tips and knuckles
    fingertips = [landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                  landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                  landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                  landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]]

    knuckles = [landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP],
                landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP],
                landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP],
                landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]]

    # Determine if the hand is open (fingertips above knuckles)
    open_fingers = sum(1 for fingertip, knuckle in zip(fingertips, knuckles) if fingertip.y < knuckle.y)

    if open_fingers >= 3:
        return "Hand Open"
    else:
        return "Hand Closed"
