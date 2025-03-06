import cv2
import numpy as np
import time  # Import the time module

# Open the thermal camera (USB or SPI)
cap = cv2.VideoCapture(0)

# Set resolution for FLIR Lepton FS (160x120)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

# Set the duration for the camera to run (in seconds)
run_duration = 120  # Change this value to set the desired run time
start_time = time.time()  # Record the start time

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a colormap for better thermal visualization
    thermal_image = cv2.applyColorMap(gray, cv2.COLORMAP_INFERNO)  # Try COLORMAP_JET, COLORMAP_HOT

    # Object segmentation using Otsu’s Thresholding
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours (objects with high heat signatures)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 100:  
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(thermal_image, (x, y), (x + w, y + h), (255, 255, 255), 2)

            # Mock temperature reading based on pixel intensity
            temp = np.mean(gray[y:y + h, x:x + w]) / 2.5 + 20  # Convert pixel value to temperature (approximate)

            # Auto-resize font based on object size
            font_scale = max(0.5, min(1.5, w / 100))
            font_thickness = max(1, int(w / 40))

            # Display temperature reading
            cv2.putText(thermal_image, f"{temp:.1f}°C", (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)
            
     # Calculate elapsed time
    elapsed_time = time.time() - start_time
    remaining_time = run_duration - elapsed_time

    # Resize window size to 640x360 while keeping the resolution at 160x120
    resized_window = cv2.resize(thermal_image, (640, 360), interpolation=cv2.INTER_NEAREST)

    # Show the resized window
    cv2.imshow("FLIR Lepton FS Thermal View", resized_window)

    # Check if the run duration has elapsed
    if time.time() - start_time >= run_duration:
        print("Run duration completed. Stopping the camera.")
        break

    # Exit on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
####
# Cleanup
cap.release()
cv2.destroyAllWindows()
