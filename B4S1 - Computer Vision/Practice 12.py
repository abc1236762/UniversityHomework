import cv2 as cv
import numpy as np

frame_start, frame_n = 19400, 600
cap = cv.VideoCapture('WiiPlay.mp4')
if not cap.isOpened():
    raise IOError("failed to open video file")
cap.set(cv.CAP_PROP_POS_FRAMES, frame_start)
ok, frame = cap.read()
if not ok:
    exit()

hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
locations, weights = hog.detectMultiScale(frame, finalThreshold=1)
trackers, are_tracked = [], []
output = frame.copy()
for (x, y, w, h) in locations:
    x, y, w, h = (int(round(x + w / 3)), int(round(y + h / 3)),
                  int(round(w / 3)), int(round(h / 3)))
    tracker = cv.TrackerMedianFlow_create()
    is_tracked = tracker.init(frame, (x, y, w, h))
    trackers.append(tracker)
    are_tracked.append(is_tracked)
    cv.rectangle(output, (x, y), (x + w - 1, y + h - 1), (0x00, 0xFF, 0x00), 2)

cv.imshow("output", output)
if cv.waitKey(1) >= 0:
    cap.release()
    cv.destroyAllWindows()
    exit()

frame_i = 0
while True:
    if frame_i > frame_n:
        cap.set(cv.CAP_PROP_POS_FRAMES, frame_start)
        frame_i = 0
    frame_i += 1
    _, frame = cap.read()
    output = frame.copy()
    for i in range(0, len(trackers)):
        are_tracked[i], bbox = trackers[i].update(frame)
        if are_tracked[i]:
            x, y, w, h = (int(round(bbox[0])), int(round(bbox[1])),
                          int(round(bbox[2])), int(round(bbox[3])))
            cv.rectangle(output, (x, y), (x + w - 1, y + h - 1), (0x00, 0x00, 0xFF), 2)
        else:
            cv.putText(output, "tracking failure detected", (40, 40),
                        cv.FONT_HERSHEY_COMPLEX, 0.5, (0x00, 0x00, 0xFF), 1)
    locations, weights = hog.detectMultiScale(frame, finalThreshold=5)
    for (x, y, w, h) in locations:
        x, y, w, h = (int(round(x + w / 3)), int(round(y + h / 3)),
                      int(round(w / 3)), int(round(h / 3)))
        cv.rectangle(output, (x, y), (x + w - 1, y + h - 1), (0x00, 0xFF, 0x00), 2)
    cv.imshow('output', output)
    if cv.waitKey(1) >= 0:
        break

cap.release()
cv.destroyAllWindows()
