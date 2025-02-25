import cv2
import numpy as np

def initialize_camera():
    cap = cv2.VideoCapture(0)  # Adjust index if needed
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
    return cap

def capture_frame(cap):
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        return None
    return frame

def release_camera(cap):
    cap.release()