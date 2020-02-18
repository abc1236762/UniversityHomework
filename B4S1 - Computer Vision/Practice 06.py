import cv2 as cv

video_capture, fps = cv.VideoCapture('WiiPlay.mp4'), 30 / 1.001
if not video_capture.isOpened():
    raise IOError("cannot open the video file")

frame_begin, frame_total = 2400, 210
video_capture.set(cv.CAP_PROP_POS_FRAMES, frame_begin)
_, frame = video_capture.read()


def threshold_image(hl, hu, sl, su, vl, vu, frame):
    if hl > hu:
        hl, hu = hu, hl
    if sl > su:
        sl, su = su, sl
    if vl > vu:
        vl, vu = vu, vl
    t = cv.inRange(frame, (hl, sl, vl), (hu, su, vu))
    return t


def pass_func(val):
    pass

cv.namedWindow('threshold')
cv.createTrackbar('H lower', 'threshold', 0x00, 0xB3, pass_func)
cv.createTrackbar('H upper', 'threshold', 0xB3, 0xB3, pass_func)
cv.createTrackbar('S lower', 'threshold', 0x00, 0xFF, pass_func)
cv.createTrackbar('S upper', 'threshold', 0xFF, 0xFF, pass_func)
cv.createTrackbar('V lower', 'threshold', 0x00, 0xFF, pass_func)
cv.createTrackbar('V upper', 'threshold', 0xFF, 0xFF, pass_func)

for i in range(0, frame_total):
    ok, frame = video_capture.read()
    if not ok:
        break
    frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    hl = cv.getTrackbarPos('H lower', 'threshold')
    hu = cv.getTrackbarPos('H upper', 'threshold')
    sl = cv.getTrackbarPos('S lower', 'threshold')
    su = cv.getTrackbarPos('S upper', 'threshold')
    vl = cv.getTrackbarPos('V lower', 'threshold')
    vu = cv.getTrackbarPos('V upper', 'threshold')
    threshold = threshold_image(hl, hu, sl, su, vl, vu, frame_hsv)
    cv.imshow('frame', frame)
    cv.imshow('threshold', threshold)
    c = cv.waitKey(round(1000 / fps))
    if c == 0x1B:
        break

video_capture.release()
cv.destroyAllWindows()
