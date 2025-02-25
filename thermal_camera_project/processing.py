import cv2
import numpy as np

def convert_to_grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def apply_colormap(gray):
    return cv2.applyColorMap(gray, cv2.COLORMAP_INFERNO)

def segment_objects(gray):
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def detect_objects(thermal_image, gray, contours):
    objects = []
    for contour in contours:
        if cv2.contourArea(contour) > 100:  
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(thermal_image, (x, y), (x + w, y + h), (255, 255, 255), 2)
            temp = np.mean(gray[y:y + h, x:x + w]) / 2.5 + 20  # Convert pixel value to temperature (approximate)
            objects.append({"x": x, "y": y, "width": w, "height": h, "temperature": round(temp, 1)})
    return objects