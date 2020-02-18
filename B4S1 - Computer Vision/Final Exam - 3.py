import cv2 as cv
import numpy as np

R, G, B = (0x00, 0x00, 0xFF), (0x00, 0xFF, 0x00), (0xFF, 0x00, 0x00)


def detect(frame, hog):  # 3B
    locs, _ = hog.detectMultiScale(frame, finalThreshold=3)
    trackers, are_tracked = [], []
    result = frame.copy()
    for (x, y, w, h) in locs:
        x, y, w, h = x + w * 1 // 10, y - h * 3 // 10, w * 8 // 10, h
        tracker = cv.TrackerMedianFlow_create()
        is_tracked = tracker.init(frame, (x, y, w, h))
        trackers.append(tracker)
        are_tracked.append(is_tracked)
        cv.rectangle(result, (x, y), (x+w, y+h), B, 2)
    return result, trackers, are_tracked


def track(frame, trackers, are_tracked):  # 3C
    result = frame.copy()
    bboxes = []
    for i in range(len(trackers)):
        are_tracked[i], bbox = trackers[i].update(frame)
        if are_tracked[i]:
            bboxes.append(bbox)
            x, y, w, h = bbox
            x, y, w, h = int(x), int(y), int(w), int(h)
            cv.rectangle(result, (x, y), (x+w, y+h), G, 2)
        else:
            bboxes.append(None)
    return result, bboxes


def find_fastest(frame, prev_bboxes, bboxes):  # 3D
    result = frame.copy()
    fastest_i, fastest_speed = -1, 0
    for i, (prev_bbox, bbox) in enumerate(zip(prev_bboxes, bboxes)):
        if prev_bbox is None or bbox is None:
            continue
        px, py, pw, ph = prev_bbox
        x, y, w, h = bbox
        pcx, pcy = px + pw / 2, py + ph / 2
        cx, cy = x + w / 2, y + h / 2
        c = ((pcx - cx) ** 2 + (pcy - cy) ** 2) ** 0.5
        if fastest_speed < c:
            fastest_speed = c
            fastest_i = i
    if fastest_i >= 0 and fastest_speed > 0.02:
        x, y, w, h = bboxes[fastest_i]
        x, y, w, h = int(x), int(y), int(w), int(h)
        cv.rectangle(result, (x, y), (x+w, y+h), R, 2)
    return result


def loop_frames(cap, frames_from, frames_to, hog):
    frames_i = frames_from
    while True:
        if frames_i > frames_to:
            frames_i = frames_from
            cap.set(cv.CAP_PROP_POS_FRAMES, frames_from)
        frames_i += 1
        ok, frame = cap.read()
        if not ok:
            break
        if frames_i - 1 == frames_from:
            result, trackers, are_tracked = detect(frame, hog)
            cv.imshow('detected', result)
            prev_bboxes, bboxes = [], []
        else:
            prev_bboxes = bboxes
            result, bboxes = track(frame, trackers, are_tracked)
            if len(prev_bboxes) > 0:
                r = find_fastest(frame, prev_bboxes, bboxes)
                cv.imshow('find_the_fastest_character', r)
            cv.imshow('tracking', result)
        if cv.waitKey(1) >= 0:
            break


def main():  # 3A
    cap = cv.VideoCapture('WiiPlay.mp4')
    frames_from, frames_to = 2480, 2600
    cap.set(cv.CAP_PROP_POS_FRAMES, frames_from)
    hog = cv.HOGDescriptor()
    hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

    loop_frames(cap, frames_from, frames_to, hog)
    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
