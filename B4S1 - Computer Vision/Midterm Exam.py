import copy
import cv2 as cv

hsv_track_bar_names = ['Hue-Min', 'Sat-Min', 'Val-Min', 'Hue-Max', 'Sat-Max', 'Val-Max']
hsv_track_bar_range = [(0x00, 0xB3), (0x00, 0xFF), (0x00, 0xFF), (0xB3, 0xB3), (0xFF, 0xFF), (0xFF, 0xFF)]
elliptical_kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
cursor_hsv_range = [59, 47, 215, 119, 143, 255]
timer_hsv_range = [23, 215, 215, 31, 255, 255]
skin_hsv_range = [11, 71, 47, 23, 159, 255]


def get_video_capture():
    video_capture, fps = cv.VideoCapture('WiiPlay.mp4'), 30 / 1.001
    if not video_capture.isOpened():
        raise IOError("cannot open the video file")
    frame_begin, frame_total = 2400, 210
    video_capture.set(cv.CAP_PROP_POS_FRAMES, frame_begin)
    return video_capture, fps, frame_total


def create_hsv_range_bar(): # 3
    cv.namedWindow('input')
    for (n, r) in zip(hsv_track_bar_names, hsv_track_bar_range):
        cv.createTrackbar(n, 'input', r[0], r[1], lambda val: None)


def get_hsv_range(): # 3
    hsv_range = []
    for n in hsv_track_bar_names:
        hsv_range.append(cv.getTrackbarPos(n, 'input'))
    return hsv_range


def threshold_image(hsv_range, frame_hsv): # 4
    ch = len(hsv_range) // 2
    for i in range(0, ch):
        j = ch + i
        if hsv_range[i] > hsv_range[j]:
            hsv_range[i], hsv_range[j] = hsv_range[j], hsv_range[i]
    threshold = cv.inRange(frame_hsv, tuple(hsv_range[:ch]), tuple(hsv_range[ch:]))
    # threshold = cv.cvtColor(cv.bitwise_and(frame_hsv, frame_hsv, mask=threshold), cv.COLOR_HSV2BGR)
    return threshold


def main():
    video_capture, fps, frame_total = get_video_capture()
    create_hsv_range_bar()
    frame_i = 0
    while True:
        if frame_i == frame_total:
            video_capture, _, _ = get_video_capture()
            frame_i = 0
        frame_i += 1
        ok, frame = video_capture.read()
        if not ok:
            break
        cv.imshow('input', frame) # 1
        frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) # 2
        hsv_range = get_hsv_range() # 3
        threshold = threshold_image(hsv_range, frame_hsv) # 4
        cv.imshow('threshold', threshold) # 4
        frame_opening = cv.morphologyEx(frame, cv.MORPH_OPEN, elliptical_kernel) # 5
        cv.imshow('test', cv.absdiff(frame, frame_opening)) # 5
        cursor_threshold = threshold_image(cursor_hsv_range, frame_hsv) # 6
        cv.imshow('cursor', cursor_threshold) # 6
        timer_threshold = threshold_image(timer_hsv_range, frame_hsv) # 7
        cv.imshow('timer', timer_threshold) # 7
        skin_threshold = threshold_image(skin_hsv_range, frame_hsv) # 8
        cv.imshow('skin', skin_threshold) # 8
        c = cv.waitKey(round(1000 / fps))
        if c == 0x1B:
            break
        elif c == 0x20:
            cv.waitKey()
    video_capture.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
