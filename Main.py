import game
import detection 
import cv2
from ultralytics import YOLO
import os



cap = cv2.VideoCapture(0)

hand_x = 60


while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Webcam frame error.")
        break
    gesture, center_x = detection.detect_gesture(frame)

    if center_x is not None:
        hand_x = center_x
    print("Gesture:", gesture)
    print("Hand X:", hand_x)

    frame = game.run_game(frame,hand_x, gesture)

    cv2.imshow("Lightning McQueen", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

