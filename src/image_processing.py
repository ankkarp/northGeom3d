import cv2
import numpy as np
import math

def euclidean_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def pixels_to_mm(pixels):
    return pixels * 0.024

def find_circle(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_radius = 20
    max_radius = 1000

    centers = []

    for contour in contours:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        if min_radius <= radius <= max_radius:
            cv2.circle(img, (int(x), int(y)), int(radius), (255, 0, 0), 2)
            centers.append((int(x), int(y)))

    for i in range(len(centers) - 1):
        cv2.line(img, centers[i], centers[i + 1], (0, 255, 0), 2)

        midpoint = ((centers[i][0] + centers[i+1][0]) // 2, (centers[i][1] + centers[i+1][1]) // 2)
        distance_px = euclidean_distance(centers[i], centers[i + 1])
        distance_mm = pixels_to_mm(distance_px)

        cv2.putText(img, f"{distance_mm:.1f}", midpoint, cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4, cv2.LINE_AA)

    return img

def find_circle_and_line(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    _, binary = cv2.threshold(blur, 140, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    min_radius = 30
    max_radius = 500

    centers = []

    for contour in contours:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        if min_radius <= radius <= max_radius:
            mask = np.zeros_like(gray)
            cv2.circle(mask, (int(x), int(y)), int(radius), 255, -1)
            mean_val = cv2.mean(gray, mask=mask)[0]
            if mean_val > 100:  # White circle
                cv2.circle(img, (int(x), int(y)), int(radius), (255, 0, 0), 2)
                
                radius_mm = pixels_to_mm(radius)

                # Display radius next to the white circle
                cv2.putText(img, f"d={radius_mm:.1f}", (int(x) - 5, int(y) - int(radius) - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 2)

            else: # Black circle
                cv2.circle(img, (int(x), int(y)), int(radius), (0, 0, 255), 4)
                centers.append((int(x), int(y)))

    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            distance_px = euclidean_distance(centers[i], centers[j])
            distance_mm = pixels_to_mm(distance_px)

            if distance_mm < 12:
                cv2.line(img, centers[i], centers[j], (0, 255, 0), 2)

                midpoint = ((centers[i][0] + centers[j][0]) // 2, (centers[i][1] + centers[j][1]) // 2)

                cv2.putText(img, f"{distance_mm:.1f}", midpoint, cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4, cv2.LINE_AA)

    return img
