import threading
import time

import cv2
import requests
import uvicorn
from fastapi import FastAPI
from ultralytics import YOLO

app = FastAPI()

last_pts = {"x": None, "y": None}
offset = 0.0

@app.post("/face-center")
async def receive_face_center(offset_x: int, offset_y: int):
    last_pts["x"] = offset_x
    last_pts["y"] = offset_y
    return {"status": "ok", "received": {"x": offset_x, "y": offset_y}}

@app.get("/face-center")
async def get_face_center():
	return {"offset_x": last_pts["x"], "offset_y": last_pts["y"]}

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")

if __name__ == "__main__":
    # Start API server in background thread
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    time.sleep(1.0)  # give server a moment to bind to port 8000

    model = YOLO(r"c:\Users\mtsag\Downloads\yolov8n-face-lindevs.pt")
    cap = cv2.VideoCapture(0)    

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        mirrored_frame = cv2.flip(frame, 1)
        results = model(mirrored_frame, verbose=False)
        annotated_frame = results[0].plot()
        cx = mirrored_frame.shape[1] // 2
        cy = mirrored_frame.shape[0] // 2
        # print(mirrored_frame.shape[1], mirrored_frame.shape[0])

        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            
			#0, 0 is center 
            offset_x = center_x - cx
            offset_y = center_y - cy
            print(offset_x, offset_y) #640-480 -> 320-240

            # cv2.circle(annotated_frame, (center_x, center_y), 6, (0, 255, 0), -1)
            # print(center_x, center_y)
            # cv2.putText(annotated_frame, "test", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            # img = cv2.putText(img, "Hello", (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            try:
                requests.post(
                    "http://127.0.0.1:8000/face-center",
                    params={"offset_x": offset_x, "offset_y": offset_y},
                    timeout=0.5,
                )
            except requests.RequestException:
                pass

        cv2.imshow("Face Tracking", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()