import cv2 as cv
import numpy as np

R, G, B = (0x00, 0x00, 0xFF), (0x00, 0xFF, 0x00), (0xFF, 0x00, 0x00)

ft_x, ft_y, ft_w, ft_h = 0, 0, 0, 0
ft_is_mouse_pressed = False
ft_first_frame = None
ft_output_frame = None


def find_target_mouse_callback(event, x, y, flags, param):  # 1B
    global ft_x, ft_y, ft_w, ft_h
    global ft_is_mouse_pressed, ft_output_frame
    if event == cv.EVENT_LBUTTONDOWN:
        ft_is_mouse_pressed = True
        ft_x, ft_y = x, y
        ft_output_frame = ft_first_frame.copy()
    elif event == cv.EVENT_MOUSEMOVE and ft_is_mouse_pressed:
        ft_output_frame = ft_first_frame.copy()
        cv.rectangle(ft_output_frame, (ft_x, ft_y), (x, y), B, 2)
    elif event == cv.EVENT_LBUTTONUP:
        ft_is_mouse_pressed = False
        ft_w, ft_h = x - ft_x, y - ft_y


def find_target(cap):  # 1B
    global ft_first_frame, ft_output_frame
    name = 'Target Finder (press any key to continue)'
    _, ft_first_frame = cap.read()
    ft_output_frame = ft_first_frame.copy()
    cv.namedWindow(name)
    cv.setMouseCallback(name, find_target_mouse_callback)
    while True:
        cv.imshow(name, ft_output_frame)
        if cv.waitKey(1) >= 0 and not ft_is_mouse_pressed and ft_w * ft_h > 0:
            break
    cv.destroyAllWindows()
    return ft_first_frame[ft_y:ft_y+ft_h, ft_x:ft_x+ft_w].copy()


def detect_target(frame, target, match_mode):  # 1C
    result = cv.matchTemplate(frame, target, match_mode)
    result = cv.normalize(result, None, 0, 255, cv.NORM_MINMAX)
    _, _, min_loc, _ = cv.minMaxLoc(result)
    result = cv.cvtColor(result, cv.COLOR_GRAY2BGR).astype(np.uint8)
    return result, min_loc


def loop_frames(cap, frames_from, frames_to, target, match_mode):
    frames_i = frames_from
    while True:
        if frames_i > frames_to:
            frames_i = frames_from
            cap.set(cv.CAP_PROP_POS_FRAMES, frames_from)
        frames_i += 1
        ok, frame = cap.read()
        if not ok:
            break
        output_frame = frame.copy()
        result, (mx, my) = detect_target(frame, target, match_mode)
        cv.rectangle(output_frame, (mx, my), (mx + ft_w, my + ft_h), R, 2)
        cv.rectangle(result, (mx - ft_w // 2, my - ft_h // 2),
                     (mx + ft_w // 2, my + ft_h // 2), G, 2)
        fh, fw = output_frame.shape[:2]
        fa = fh / fw
        fw = fw // 2
        output_frame = cv.resize(
            output_frame, (fw, int(fw * fa)), interpolation=cv.INTER_AREA)
        result = cv.resize(
            result, (fw, int(fw * fa)), interpolation=cv.INTER_AREA)
        cv.imshow('find_this_mii', np.hstack((output_frame, result)))
        if cv.waitKey(1) >= 0:
            break


def main():  # 1A
    cap = cv.VideoCapture('WiiPlay.mp4')
    frames_from, frames_to = 4820, 5000
    match_mode = cv.TM_SQDIFF_NORMED
    cap.set(cv.CAP_PROP_POS_FRAMES, frames_from)
    target = find_target(cap)
    loop_frames(cap, frames_from, frames_to, target, match_mode)
    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
