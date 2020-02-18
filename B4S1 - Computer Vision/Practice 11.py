import cv2 as cv
import numpy as np

def move_image(img, tx, ty):
    ih, iw = img.shape[:2]
    mat = np.float64([[1, 0, tx],[0, 1, ty]])
    return cv.warpAffine(img, mat, (iw, ih))

cap = cv.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError('unable to open the camera')
face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
if face_cascade.empty():
    raise IOError('unable to load cascade classifier xml file')

while True:
    ok, frame = cap.read()
    if not ok:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=9)
    if len(faces) > 0:
        h, w, c = frame.shape
        fx, fy, fw, fh = faces[0]
        dx, dy = fx - w / 2 + fw / 2, fy - h / 2 + fh / 2
        gk_x = cv.getGaussianKernel(w, fw / 4)
        gk_y = cv.getGaussianKernel(h, fh / 4)
        gk = gk_y * gk_x.T
        mask = cv2.normalize(gk, None, 0, 1, cv2.NORM_MINMAX)
        mask = move_image(mask, dx, dy)
        for i in range(c):
            frame[:, :, i] = frame[:, :, i] * mask
    else:
        frame = np.zeros(frame.shape, dtype=np.uint8)
    cv.imshow('frame', frame)
    if cv.waitKey(1) >= 0:
        break

cap.release()
cv.destroyAllWindows()
