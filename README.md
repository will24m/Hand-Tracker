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

Hand-Tracker/ ├── gui/ │ └── app_interface.py # Main GUI and control logic for hand tracking. ├── utils/ │ └── hand_recognition.py # Core hand recognition and gesture classification logic. ├── hand_tracker.py # Real-time video processing, hand tracking, and gesture detection. ├── gesture_log.txt # Logs all detected gestures with timestamps. ├── README.md # Comprehensive project documentation (this file!).

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

Or install manually:
pip install opencv-python mediapipe pyttsx3 grlib
