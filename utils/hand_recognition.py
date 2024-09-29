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
        num_fingers_raised = 0

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw landmarks and connections
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Check if the hand is open or closed
                open_status = classify_hand_gesture(hand_landmarks)

                # Count how many fingers are raised
                num_fingers_raised = count_raised_fingers(hand_landmarks)
                
                # Combine status for open/closed and fingers raised
                status = f"{open_status}, Fingers Raised: {num_fingers_raised}"

        return frame, status

def classify_hand_gesture(landmarks):
    """Classifies whether the hand is open or closed."""
    # Check if fingertips are above knuckles (open hand gesture)
    fingertips = [landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                  landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                  landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                  landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]]

    knuckles = [landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP],
                landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP],
                landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP],
                landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]]

    open_fingers = sum(1 for fingertip, knuckle in zip(fingertips, knuckles) if fingertip.y < knuckle.y)

    if open_fingers >= 3:
        return "Hand Open"
    else:
        return "Hand Closed"

def count_raised_fingers(landmarks):
    """Counts how many fingers are raised based on the landmark positions."""
    # Define the landmarks for the tips of each finger
    finger_tips = [mp_hands.HandLandmark.THUMB_TIP,
                   mp_hands.HandLandmark.INDEX_FINGER_TIP,
                   mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                   mp_hands.HandLandmark.RING_FINGER_TIP,
                   mp_hands.HandLandmark.PINKY_TIP]

    # Define the landmarks for the knuckles of each finger
    finger_knuckles = [mp_hands.HandLandmark.THUMB_IP,
                       mp_hands.HandLandmark.INDEX_FINGER_MCP,
                       mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
                       mp_hands.HandLandmark.RING_FINGER_MCP,
                       mp_hands.HandLandmark.PINKY_MCP]

    raised_fingers = 0

    # Check each finger: if the tip is above the knuckle, consider the finger raised
    for tip, knuckle in zip(finger_tips, finger_knuckles):
        if landmarks.landmark[tip].y < landmarks.landmark[knuckle].y:  # Tip is higher than the knuckle
            raised_fingers += 1

    return raised_fingers
