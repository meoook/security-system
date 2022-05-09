import cv2
import time
import datetime

import numpy as np

_resolution = 800, 600
# _resolution = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, _resolution[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, _resolution[1])

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

ui_color = (0, 255, 0)
ui = np.zeros((30, _resolution[0], 3), np.uint8)
cv2.line(ui, (0, 0), (ui.shape[1], 0), ui_color, 1)
ui_author = "author: meok"
cv2.putText(ui, ui_author, (ui.shape[1]-len(ui_author)*9, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, ui_color, 1)

# ui[:] = 0, 255, 0

while True:
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) + len(bodies) > 0:
        if detection:
            timer_started = False
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20, _resolution)
            print("Started Recording!")
    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = Falsea
                out.release()
                print('Stop Recording!')
        else:
            timer_started = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)

    for (x, y, width, height) in faces:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)

    # cv2.addText(frame, "author: meok", (10, 15), 'arial', 1, (0, 255, 0), 1)

    picture = np.vstack((frame, ui))  # Join camera and ui

    cv2.imshow("Security system", picture)

    if cv2.waitKey(1) == ord('q'):
        break


out.release()
cap.release()
cv2.destroyAllWindows()
