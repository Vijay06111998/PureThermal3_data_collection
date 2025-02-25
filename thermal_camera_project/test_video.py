import cv2

cap = cv2.VideoCapture(0)  # Try to open the default camera
if not cap.isOpened():
    print("Error: Could not access the camera.")
else:
    print("Camera opened successfully!")
    cap.release()
