# OpenCV Face Tracker

This project combines a Python face-tracking app with an ESP32 sketch that reads face offsets over HTTP and drives two servos.

## Demo Video

[Watch the demo video](face_computer_view.mp4)

<!-- <video controls width="720" src="demo/demo.mp4"></video> -->
<video controls src="demo/face_computer_view.mp4"></video>

## Project Files

- [faceTracker.py](faceTracker.py) starts the FastAPI endpoint, runs the face detector, and posts face-center offsets.
- [sketch_jun14a/sketch_jun14a.ino](sketch_jun14a/sketch_jun14a.ino) reads the offsets and moves the servos.

## Notes

- Update the YOLO model path in `faceTracker.py` before running.
- Update the Wi-Fi credentials and server URL in the Arduino sketch before uploading it to the board.