# OpenCV Face Tracker

This project combines a Python face-tracking app with an ESP32 sketch that reads face offsets over HTTP and drives two servos.

## Demo Video

<video controls src="demo/face_computer_view.mp4" title="Demo Video"></video>
[![Face Tracker Demo](https://img.youtube.com/vi/c_oRC56zAxI/maxresdefault.jpg)](https://youtu.be/c_oRC56zAxI)

## Project Files

- [faceTracker.py](faceTracker.py) starts the FastAPI endpoint, runs the face detector, and posts face-center offsets.
- [sketch_jun14a/sketch_jun14a.ino](sketch_jun14a/sketch_jun14a.ino) reads the offsets and moves the servos.

## Notes

- Update the YOLO model path in `faceTracker.py` before running.
- Update the Wi-Fi credentials and server URL in the Arduino sketch before uploading it to the board.