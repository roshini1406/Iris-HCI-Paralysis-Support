 👁️ Iris-Based Human-Computer Interaction for Paralyzed Patients

An AI-powered assistive technology (HCI) designed to help individuals with severe motor impairments or paralysis interact with computers. This system allows users to control the mouse cursor and communicate using only their eye movements and blinks.



 🚀 Features
* **Iris-Based Cursor Control**: Uses MediaPipe Face Mesh to track iris landmarks and move the mouse cursor smoothly across the screen.
* **Blink-to-Click**: Detects blinks using the Eye Aspect Ratio (EAR) with a 0.28 threshold; a blink lasting longer than 0.15 seconds triggers a mouse click.
* **Emergency SOS System**: Integrated with **Twilio API** to send an emergency SMS to a caregiver when the "I need help" phrase is selected.
* **Voice Feedback (TTS)**: Uses `pyttsx3` to announce selected phrases out loud, providing a voice for the user.
* **Interactive Communication Board**: A custom Tkinter-based GUI featuring quick-access phrases and a full virtual keyboard for typing.



 🛠️ Tech Stack
* Core Logic: Python
* Computer Vision: OpenCV, MediaPipe
* Automation: PyAutoGUI
* GUI Framework: Tkinter
* APIs: Twilio (SMS), pyttsx3 (Text-to-Speech)



📋 Prerequisites
Before running the application, ensure you have a webcam and install the following Python libraries:

```bash
pip install opencv-python mediapipe pyautogui pyttsx3 twilio
