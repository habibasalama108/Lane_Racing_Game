import cv2
import os
from ultralytics import YOLO

possible_paths = [
    "best.pt",
    "runs/detect/train/weights/best.pt",
    "runs/detect/train2/weights/best.pt",
    "runs/detect/train3/weights/best.pt",
    "weights/best.pt"
]

model_path = None
for path in possible_paths:
    if os.path.exists(path):
        model_path = path
        break

if model_path is None:
    print("ERROR: Could not find best.pt! Make sure training finished.")
    exit()

print(f"Successfully loaded model from: {model_path}")
model = YOLO(model_path)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Webcam frame error.")
        break

    results = model(frame, conf=0.4)
    annotated_frame = results[0].plot()

    cv2.imshow("Gesture Detection Test", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()