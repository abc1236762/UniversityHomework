import cv2 as cv
cap = cv.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Failed to open the webcam.")

_, first_img = cap.read()
while True:
    _, img = cap.read()
    diff_img = cv.absdiff(img , first_img)
    cv.imshow('Capture', diff_img)
    if cv.waitKey(1) == 0x1B:
        break

cap.release()
cv.destroyAllWindows()
