# **Hand Gesture Recognition System - Advanced**

## Overview
Welcome to the **Hand Gesture Recognition System**, a powerful, open-source project designed to track and recognize hand gestures using computer vision and machine learning techniques. Leveraging state-of-the-art libraries such as **OpenCV**, **MediaPipe**, and **GRLib** for gesture classification, this project goes beyond basic hand tracking to deliver an intelligent and interactive experience.

This system captures live video, tracks the user's hand movements in real-time, and classifies complex hand gestures such as "Thumbs Up", "Peace Sign", or "Fist". It also provides dynamic visual and audio feedback, gesture logging, and user-friendly features like gesture-based controls.

---

## Features

### 🚀 **Core Functionalities:**
- **Real-time Hand Tracking**: Uses your webcam to capture live video and detect hand gestures on the fly.
- **Gesture Recognition**: Recognizes common gestures like open hand, closed fist, thumbs up, peace sign, and more using **MediaPipe** and **GRLib**.
- **Visual Feedback**: Provides real-time feedback with hand landmarks drawn on the video feed, along with gesture status text.
- **Multi-Hand Detection**: Detects and tracks multiple hands simultaneously, providing individual status updates for each.
- **Dynamic Gesture Controls**: Execute commands such as starting or stopping the hand tracker through gestures (e.g., thumbs up to start tracking, fist to stop).
- **Audio Feedback**: Uses text-to-speech to give real-time voice feedback when a gesture is detected, enhancing the interactive experience.
- **Gesture Logging**: Saves a detailed log of detected gestures along with timestamps to a file, useful for tracking user interactions.
  
---
abahahahahahahahahahahahaa
### 🛠 **Technologies Used:**
1. **OpenCV**:
   - Provides real-time video processing and visual feedback.
   - Used for drawing hand landmarks and gesture statuses on the video feed.

2. **Google MediaPipe**:
   - Responsible for detecting hand landmarks and interpreting basic hand gestures (open/closed).
   - Provides robust hand tracking even under varying conditions.

3. **GRLib (Gesture Recognition Library)**:
   - Enhances the gesture classification capabilities by allowing for the recognition of more complex gestures.
   - Trained with a custom dataset to classify gestures like thumbs up, peace sign, and more.

4. **Text-to-Speech (pyttsx3)**:
   - Provides real-time voice feedback based on recognized gestures.

5. **Multi-threading with Python**:
   - Ensures the application remains responsive while processing video in the background.

6. **Logging**:
   - Uses Python’s logging library to store recognized gestures with timestamps.

---

### 📂 **Project Structure:**

Hand-Tracker/ ├── gui/ │ └── app_interface.py # Main interface controlling the hand tracker and managing the GUI. ├── utils/ │ └── hand_recognition.py # Contains logic for hand gesture detection and classification. ├── hand_tracker.py # Real-time video processing, hand tracking, and gesture detection. ├── gesture_log.txt # Logs all detected gestures with corresponding timestamps. ├── README.md # Comprehensive project documentation (this file!).

yaml
Copy code

---

## Setup

### 1. **Prerequisites**
- **Python 3.8+**
- A working webcam.
- Internet connection for downloading dependencies.

### 2. **Install Dependencies**
Use the following command to install all required Python libraries:
```bash
pip install -r requirements.txt
```
```Or install manually:

pip install opencv-python mediapipe pyttsx3 grlib
```
How It Works
Hand Tracking and Recognition:
Frame Capture: The system captures each video frame from your webcam.
Hand Detection: Each frame is processed using MediaPipe to detect hand landmarks (21 points on the hand).
Gesture Classification: The hand’s position and finger movements are analyzed by GRLib to classify complex gestures like "Thumbs Up", "Peace Sign", and "Fist".
Feedback: Visual feedback (e.g., text and drawings) is shown on the video feed, and audio feedback is provided for detected gestures.
Gesture Logging: Each gesture is logged with a timestamp for future analysis.
Detailed Example
Let’s walk through an example interaction:

User Action: You raise your hand in front of the camera and show a "Thumbs Up".
System Response:
The system detects your hand, recognizes the "Thumbs Up" gesture.
A green rectangle appears around your hand, and the text "Thumbs Up" is displayed.
The system says “Thumbs Up detected” via audio feedback.
The gesture and timestamp are logged in gesture_log.txt.
Advanced Features
1. Gesture-Based Controls:
Use gestures to control the system:

Thumbs Up: Starts the tracker.
Fist: Stops tracking.
Peace Sign: Saves a screenshot of the current frame.
2. Multi-Hand Detection:
The system can detect and track multiple hands at once. For each hand, the system:

Detects gestures separately.
Provides individual status feedback.
3. Virtual Drawing Mode (Experimental):
Use your hand as a virtual pen:

Move your index finger to draw on the screen.
Close your fist to stop drawing.
Customization
Adding New Gestures:
You can train the system to recognize new gestures using GRLib:

Record hand landmarks for the desired gesture.
Feed the data into GRLib’s dynamic detector.
Update the classification logic to recognize the new gesture.
Performance Optimization
Frame Rate Counter: Monitors the system’s frame rate to ensure optimal performance. Adjusts processing speed dynamically.
Error Handling: Automatically handles cases where the camera is disconnected or gestures can’t be detected.
Future Improvements
Integration with IoT Devices: Control smart home appliances using gestures.
Enhanced Gesture Vocabulary: Incorporate sign language recognition.
Mobile App Version: Extend the project to mobile devices using TensorFlow Lite.
Contributing
Contributions are welcome! Feel free to submit issues, fork the project, and send pull requests.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
Google MediaPipe for providing robust hand tracking tools.
GRLib for advanced gesture classification.
OpenCV for enabling efficient real-time video processing.
