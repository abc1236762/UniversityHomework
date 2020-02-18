import cv2 as cv

video_capture, fps, size = cv.VideoCapture('WiiPlay.mp4'), 29.97, (1280, 720)
video_stream_format = cv.VideoWriter_fourcc(*'x264')
if not video_capture.isOpened():
    raise IOError("cannot open the video file")
video_stream = cv.VideoWriter('410521209.mp4', video_stream_format, fps, size)

frame_begin, frame_total = 2400, 210
video_capture.set(cv.CAP_PROP_POS_FRAMES, frame_begin)
_, frame = video_capture.read()

init_tracking_bbox, tracking_range = (50, 300, 80, 100), (0.8, 1.2)
tracker = cv.TrackerTLD_create()
tracker.init(frame, init_tracking_bbox)

for i in range(0, frame_total):
    ok, frame = video_capture.read()
    if not ok:
        break
    ok, tracking_bbox = tracker.update(frame)
    if ok and        tracking_bbox[2] >= init_tracking_bbox[2] * tracking_range[0] and        tracking_bbox[2] <= init_tracking_bbox[2] * tracking_range[1] and        tracking_bbox[3] >= init_tracking_bbox[3] * tracking_range[0] and        tracking_bbox[3] <= init_tracking_bbox[3] * tracking_range[1]:
        pt1 = (int(tracking_bbox[0]), int(tracking_bbox[1]))
        pt2 = (int(tracking_bbox[0] + tracking_bbox[2]),
               int(tracking_bbox[1] + tracking_bbox[3]))
        cv.rectangle(frame, pt1, pt2, (0xFF, 0x00, 0x00), 2)
    cv.imshow('frame', frame)
    video_stream.write(frame)
    c = cv.waitKey(round(1000 / fps))
    if c == 0x1B:
        break

video_capture.release()
video_stream.release()
cv.destroyAllWindows()
