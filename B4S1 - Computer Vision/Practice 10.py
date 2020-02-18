import sys
import cv2 as cv
import numpy as np

face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade =  cv.CascadeClassifier('haarcascade_eye.xml')
mouth_cascade = cv.CascadeClassifier('haarcascade_mcs_mouth.xml')
if face_cascade.empty() or mouth_cascade.empty() or mouth_cascade.empty():
    raise IOError('unable to load cascade classifier xml file')

cap = cv.VideoCapture(0)
hat = cv.imread('hat.png', cv.IMREAD_UNCHANGED)
mst = cv.imread('mustache.png', cv.IMREAD_UNCHANGED)

def draw_hat(frame, eye1_c, eye2_c):
    hat_c = hat.copy()
    hat_i = hat_c[:, :, 0:3].astype(np.float64)
    hat_a = hat_c[:, :, 3:4].astype(np.float64) / 0xFF
    hat_i *= hat_a
    hat_h, hat_w = hat_i.shape[:2]
    ecx, ecy = (eye1_c[0] + eye2_c[0]) / 2, (eye1_c[1] + eye2_c[1]) / 2

    return frame

while True:
    ok, frame = cap.read()
    if not ok:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=12)
    for (fx, fy, fw, fh) in faces:
        frame_face = frame[fy:fy+fh, fx:fx+fw]
        gray_face = gray[fy:fy+fh, fx:fx+fw]
        fhh = int(fh / 2)
        gray_face_u = gray_face[0:fhh, :]
        gray_face_d = gray_face[fhh:fh, :]
        eyes = eye_cascade.detectMultiScale(gray_face_u, scaleFactor=1.2, minNeighbors=6)
        if len(eyes) == 2:
            eye1, eye2 = eyes[0], eyes[1]
            eye1[0], eye1[1] = fx + eye1[0], fy + eye1[1]
            eye2[0], eye2[1] = fx + eye2[0], fy + eye2[1]
            eye1_c = np.array(eye1[0] + eye1[2] / 2, eye1[1] + eye1[3] / 2)
            eye2_c = np.array(eye2[0] + eye2[2] / 2, eye2[1] + eye2[3] / 2)
            frame = draw_hat(frame, eye1_c, eye2_c)
        mouths = mouth_cascade.detectMultiScale(gray_face_d, scaleFactor=1.2, minNeighbors=6)
        if len(mouths) == 1:
            mx, my, mw, mh = mouths[0]
            # mx, my = fx + mx, fy + fhh + my
            # mcx, mcy = int(mx + mh / 2), int(my + mh / 2)
            # cv.circle(frame, (mcx, mcy), 2, (0, 255, 0), 2)
    cv.imshow('frame', frame)
    c = cv.waitKey(1)
    if c == 27:
        break

cap.release()
cv.destroyAllWindows()
