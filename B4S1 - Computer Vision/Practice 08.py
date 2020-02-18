import cv2 as cv
import numpy as np


def show_edge_val(event, x, y, flags, *userdata):
    if event != cv.EVENT_MOUSEMOVE:
        return
    cv.rectangle(frame, (0, 0), (360, 24), (0, 0, 0), -1)
    msg = f'x:{x} y:{y} val:{edge[y][x]}'
    cv.putText(frame, msg, (0, 16),
               cv.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))
    cv.imshow('frame', frame)

edge: np.ndarray = None
cv.namedWindow('frame')
cap = cv.VideoCapture(0)
if not cap.isOpened():
    raise IOError("video capture cannot be opened")

while True:
    frame = cv.flip(cap.read()[1], 1)
    gray = np.float32(cv.cvtColor(frame, cv.COLOR_BGR2GRAY))
    edge = cv.cornerHarris(gray, 3, 3, 0.04)
    edge = cv.dilate(edge, None)
    cv.setMouseCallback('frame', show_edge_val)
    frame[edge > 0.01 * edge.max()] = [0, 0, 255]
    cv.imshow('frame', frame)
    if cv.waitKey(1) >= 0:
        break

cap.release()
cv.destroyAllWindows()
