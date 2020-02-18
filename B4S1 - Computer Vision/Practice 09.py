import cv2 as cv
import numpy as np

frame_start, frame_n = 4820, 180

cap = cv.VideoCapture('WiiPlay.mp4')
if not cap.isOpened():
    raise IOError("failed to open video file")
cap.set(cv.CAP_PROP_POS_FRAMES, frame_start)

_, frame = cap.read()
preview, is_mouse_pressed = np.copy(frame), False
x1 = y1 = w = h = 0


def mouse_callback(event, x, y, flags, *param):
    global preview, x1, y1, w, h, is_mouse_pressed
    if event == cv.EVENT_LBUTTONDOWN:
        is_mouse_pressed = True
        x1, y1 = x, y
        preview = np.copy(frame)
    elif event == cv.EVENT_MOUSEMOVE:
        if is_mouse_pressed:
            preview = np.copy(frame)
            cv.rectangle(preview, (x1, y1), (x, y), (0xFF, 0, 0), 2)
    elif event == cv.EVENT_LBUTTONUP:
        is_mouse_pressed = False
        w, h = x - x1, y - y1


cv.namedWindow('choose template')
cv.setMouseCallback('choose template', mouse_callback)

while True:
    cv.imshow('choose template', preview)
    if cv.waitKey(1) == 32 and not is_mouse_pressed and w * h > 0:
        break
cv.destroyAllWindows()

template = np.copy(frame[y1:y1+h, x1:x1+w])
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
           'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
method_i, frame_i = 0, 0
method = methods[method_i]

while True:
    if frame_i > frame_n:
        cap.set(cv.CAP_PROP_POS_FRAMES, frame_start)
        frame_i = 0
        method_i = (method_i + 1) % len(methods)
        method = methods[method_i]
    frame_i += 1
    _, frame = cap.read()
    result = cv.matchTemplate(frame, template, eval(method))
    print(f'result     min:{np.min(result)} max:{np.max(result)}')
    result = cv.normalize(result, None, 0, 1, cv.NORM_MINMAX)
    print(f'normalized min:{np.min(result)} max:{np.max(result)}')
    max_val, min_val, max_loc, min_loc = cv.minMaxLoc(result)
    result_dup = cv.resize(np.copy(result), (frame.shape[1], frame.shape[0])) * 255.0
    result_dup = cv.cvtColor(result_dup, cv.COLOR_GRAY2BGR).astype(np.uint8)
    cv.rectangle(result_dup, (max_loc[0] - int(w/2), max_loc[1] - int(h/2)),
                 (max_loc[0] + int(w/2), max_loc[1] + int(h/2)), (0, 0, 0), 1)
    cv.putText(result_dup, method, (0, 30),
               cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    frame_dup = np.copy(frame)
    print(frame_dup.shape, result_dup.shape)
    output = np.hstack((frame_dup, result_dup))
    cv.imshow('output', output)
    if cv.waitKey(1) == 27:
        break

cap.release()
cv.destroyAllWindows()
