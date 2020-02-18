import cv2 as cv
cap = cv.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Failed to open the webcam.")

db_alpha = 0.5
_, first_frame = cap.read()
last_frame = db_frame = first_frame

while True:
    ok, frame = cap.read()
    if not ok:
        break
    # dynamic background
    db_frame = cv.addWeighted(db_frame, db_alpha, frame, 1.0 - db_alpha, 0)
    # background subtraction
    bs_frame = cv.absdiff(frame, first_frame)
    # temporal subtraction
    ts_frame = cv.absdiff(frame, last_frame)
    last_frame = frame
    cv.imshow('dynamic background', db_frame)
    cv.imshow('background subtraction', bs_frame)
    cv.imshow('temporal subtraction', ts_frame)
    if cv.waitKey(1) == 0x1B:
        break

cap.release()
cv.destroyAllWindows()
