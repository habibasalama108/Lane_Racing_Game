import cv2
import os 
from ultralytics import YOLO 





model = YOLO("weights/best.pt") 



def detect_gesture(frame):
    results = model(frame, conf=0.4)

    result = results[0]
    boxes = result.boxes

    # No detection
    if len(boxes) == 0:
        return None, None

    # Get first detected box
    box = boxes.xyxy[0]

    x1 = float(box[0])
    y1 = float(box[1])
    x2 = float(box[2])
    y2 = float(box[3])

    # Center of detected hand
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    # Get class
    class_id = int(boxes.cls[0])

    if class_id == 0:
        gesture = "steer"
    elif class_id == 1:
        gesture = "kachow"
    else:
        gesture = None


    return gesture, center_x,



