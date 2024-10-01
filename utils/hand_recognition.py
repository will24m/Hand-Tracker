import cv2
import mediapipe as mp
import math

# Initialize MediaPipe components
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def calculate_distance(point1, point2):
    """Helper function to calculate the Euclidean distance between two points."""
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

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
    """Classifies whether the hand is open or closed with refined thumb logic."""
    
    # Calculate the center of the palm (average of wrist, middle MCP, and index MCP)
    palm_center = landmarks.landmark[mp_hands.HandLandmark.WRIST]

    # Thumb-specific detection
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    
    # Calculate distance between thumb tip/IP and palm center
    thumb_distance = calculate_distance(thumb_tip, palm_center)
    thumb_folded = thumb_distance < calculate_distance(thumb_ip, palm_center)  # Thumb is considered closed if it's folded inwards

    # Check how many fingers are open (excluding the thumb)
    finger_tips = [landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                   landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                   landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                   landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]]
    
    finger_knuckles = [landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP],
                       landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP],
                       landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP],
                       landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]]
    
    open_fingers = sum(1 for tip, knuckle in zip(finger_tips, finger_knuckles) if tip.y < knuckle.y)

    # Add thumb status to the open finger count
    if not thumb_folded:
        open_fingers += 1

    # Classify hand status based on open fingers
    if open_fingers == 0:
        return "Fist Closed"
    elif open_fingers >= 3:
        return "Hand Open"
    else:
        return "Partially Open Hand"

def count_raised_fingers(landmarks):
    """Refined method to count how many fingers are raised with thumb consideration."""
    # Define the landmarks for the tips of each finger
    finger_tips = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]

    # Define the landmarks for the knuckles of each finger
    finger_knuckles = [
        mp_hands.HandLandmark.THUMB_IP,
        mp_hands.HandLandmark.INDEX_FINGER_MCP,
        mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
        mp_hands.HandLandmark.RING_FINGER_MCP,
        mp_hands.HandLandmark.PINKY_MCP
    ]

    raised_fingers = 0

    # Use more sophisticated distance threshold for determining raised fingers
    for tip, knuckle in zip(finger_tips, finger_knuckles):
        if landmarks.landmark[tip].y < landmarks.landmark[knuckle].y and abs(landmarks.landmark[tip].x - landmarks.landmark[knuckle].x) < 0.1:  # Tip is higher and close to the knuckle horizontally
            raised_fingers += 1

    return raised_fingers
