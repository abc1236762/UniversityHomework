import itertools

import cv2 as cv

R, G, B = (0x00, 0x00, 0xFF), (0x00, 0xFF, 0x00), (0xFF, 0x00, 0x00)


def find_two_similar_faces(frame, locs, match_mode):  # 2D
    faces, xy_of_faces, frame = [], [], frame.copy()
    for x, y, w, h in locs:
        x0, x1, y0, y1 = x+w//6, x+w*5//7, y-5, y+h//6
        faces.append(frame[y0:y1, x0:x1].copy())
        xy_of_faces.append((x0, x1, y0, y1))
    mv, selected_index = 0.88, (-1, -1)
    for i, j in itertools.combinations(range(len(faces)), 2):
        face_i, face_j = faces[i], faces[j]
        try:
            result = cv.matchTemplate(face_i, face_j, match_mode)
        except:
            continue
        r_mv, _, _, _ = cv.minMaxLoc(result)
        if (mv < r_mv):
            mv, selected_index = r_mv, (i, j)
    if selected_index[0] >= 0 and selected_index[1] >= 0:
        i, j = selected_index
        fix0, fix1, fiy0, fiy1 = xy_of_faces[i]
        fjx0, fjx1, fjy0, fjy1 = xy_of_faces[j]
        cv.rectangle(frame, (fix0, fiy0), (fix1, fiy1), R, 2)
        cv.rectangle(frame, (fjx0, fjy0), (fjx1, fjy1), R, 2)
        cv.imshow('find_two_look_alike', frame)


def detect(frame, frames_i, hog, match_mode):  # 2B,2C
    result = frame.copy()
    if frames_i <= 2210:
        return result
    locs, w = hog.detectMultiScale(result, finalThreshold=3)
    find_two_similar_faces(frame, locs, match_mode)
    for x, y, w, h in locs:
        cv.rectangle(result, (x, y-h//4), (x+w, y+h), G, 2)
        cv.rectangle(result, (x+w//6, y-h//6), (x+w*5//6, y+h//6), B, 2)
    return result


def loop_frames(cap, frames_from, frames_to, hog, match_mode):
    frames_i = frames_from
    while True:
        if frames_i > frames_to:
            frames_i = frames_from
            cap.set(cv.CAP_PROP_POS_FRAMES, frames_from)
        frames_i += 1
        ok, frame = cap.read()
        if not ok:
            break
        result = detect(frame, frames_i, hog, match_mode)
        cv.imshow('pedestrians_faces', result)
        if cv.waitKey(1) >= 0:
            break


def main():  # 2A
    cap = cv.VideoCapture('WiiPlay.mp4')
    frames_from, frames_to = 2180, 2380
    match_mode = cv.TM_CCORR_NORMED
    cap.set(cv.CAP_PROP_POS_FRAMES, frames_from)
    hog = cv.HOGDescriptor()
    hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
    loop_frames(cap, frames_from, frames_to, hog, match_mode)
    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
