import cv2
import os
import time

webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Camera not working")
    exit()

while True:
    ret1, frame1 = webcam.read()
    ret2, frame2 = webcam.read()

    if not ret1 or not ret2:
        break

    # Find difference between two frames
    diff = cv2.absdiff(frame1, frame2)

    # Convert to grayscale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Dilate to fill gaps
    dilated = cv2.dilate(thresh, None, iterations=3)

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue

        motion_detected = True

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 0, 255), 2)

    if motion_detected:
        print("Motion Detected!")
        os.system("afplay /System/Library/Sounds/Glass.aiff")
        time.sleep(1)  # prevent continuous sound

    cv2.imshow("Security Camera", frame1)

    if cv2.waitKey(10) == 27:  # Press ESC to exit
        break

webcam.release()
cv2.destroyAllWindows()