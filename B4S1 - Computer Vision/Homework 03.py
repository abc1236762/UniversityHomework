import sys
import glob
from os import path

import cv2 as cv
import numpy as np


def find_haarcascades_path():
    # 尋找haarcascades的路徑，因為OpenCV可能內建
    if hasattr(cv, 'data'):
        return cv.data.haarcascades
    cv_file = path.realpath(cv.__file__)
    matched = glob.glob(path.normpath(
        f'{cv_file}/../../../../share/OpenCV/haarcascades'))
    if len(matched) > 0:
        return matched[0]
    matched = glob.glob(path.normpath(
        f'{cv_file}/../../../../share/opencv*/haarcascades'))
    if len(matched) > 0:
        return matched[0]


def read_haarcascade(haarcascades_path, target):
    # 讀取haarcascade
    haarcascades_path = haarcascades_path.strip()
    haarcascade_filename = f'haarcascade_{target}.xml'
    haarcascade_path = path.join(haarcascades_path, haarcascade_filename)
    cascade = cv.CascadeClassifier(haarcascade_path)
    if cascade.empty() and len(haarcascades_path) > 0:
        cascade = cv.CascadeClassifier(haarcascade_filename)
    if cascade.empty():
        msg = f'unable to load "{haarcascade_path}"'
        if len(haarcascades_path) > 0:
            msg += f'\nunable to load "{haarcascade_filename}"'
        raise IOError(msg)
    return cascade


def get_cp(img_or_w, h=None):
    # 取得圖片或長寬的中心點
    if h is None:
        h, w = img_or_w.shape[:2]
    else:
        w = img_or_w
    return ((w - 1) / 2, (h - 1) / 2)


def add_pair(p1, p2):
    # 相加兩個配對
    return(p1[0] + p2[0], p1[1] + p2[1])


def read_obj(file_path, w, h):
    # 讀取物件，例如帽子或鬍子，放大至可以填滿畫面大小並擴展成畫面大小，方便操作
    obj = cv.imread(file_path, cv.IMREAD_UNCHANGED)
    max_rate = max(w, h) / max(obj.shape[:2])
    min_rate = min(w, h) / min(obj.shape[:2])
    obj = resize_image(obj, min(max_rate, min_rate))
    obj = extend_image(obj, w, h)
    return obj


def draw_text(img, text, x, y, size, color, align: int = 0):
    # 描繪文字
    if not 0 <= align < 9:
        raise OverflowError
    font = cv.FONT_HERSHEY_DUPLEX
    (text_w, text_h), base_line = cv.getTextSize(text, font, size, 1)
    w, h = text_w + base_line / 2, text_h + base_line
    if align % 3 == 0:
        x = int(np.floor(x + base_line / 4))
    elif align % 3 == 1:
        x = int(round(x - w / 2 + 1 / 2 + base_line / 4))
    else:
        x = int(np.ceil(x - w + 1 + base_line / 4))
    if align // 3 == 0:
        y = int(round(y + text_h + base_line / 2 - 1))
    elif align // 3 == 1:
        y = int(round(y - h / 2 + 1 / 2 + text_h + base_line / 2 - 1))
    else:
        y = int(round(y - h + 1 + text_h + base_line / 2 - 1))
    cv.putText(img, text, (x, y), font, size, color, 1, cv.LINE_AA)


def detect_scales(gray, cascade, scale_factor=1.1, min_neighbors=6):
    # 偵測
    return cascade.detectMultiScale(
        gray, scaleFactor=scale_factor, minNeighbors=min_neighbors)


def resize_image(img, scale):
    # 調整圖片大小
    h, w = img.shape[:2]
    w, h = int(np.around(w * scale)), int(np.around(h * scale))
    return cv.resize(img, (w, h), interpolation=cv.INTER_CUBIC)


def move_image(img, dx, dy):
    # 移動圖片
    ih, iw = img.shape[:2]
    mat = np.float64([[1, 0, dx], [0, 1, dy]])
    return cv.warpAffine(img, mat, (iw, ih))


def extend_image(img, w, h):
    # 向四周擴展圖片
    ih, iw, ic = img.shape
    assert w >= iw and h >= ih
    extended = np.zeros((h, w, ic), dtype=np.uint8)
    extended[:ih, :iw, :ic] = img
    ecx, ecy = get_cp(extended)
    icx, icy = get_cp(iw, ih)
    extended = move_image(extended, ecx - icx, ecy - icy)
    return extended


def scale_image(img, cp, scale):
    # 縮放圖片
    ih, iw = img.shape[:2]
    mat = cv.getRotationMatrix2D(cp, 0, scale)
    return cv.warpAffine(img, mat, (iw, ih))


def rotate_image(img, cp, angle):
    # 旋轉圖片
    ih, iw = img.shape[:2]
    mat = cv.getRotationMatrix2D(cp, angle, 1)
    return cv.warpAffine(img, mat, (iw, ih))


def blend_image(fg_bgra, bg_bgr):
    # 合成圖片
    img = fg_bgra[:, :, :3].astype(np.float64)
    fg_a = fg_bgra[:, :, 3:].astype(np.float64) / 0xFF
    return (img * fg_a + bg_bgr * (1 - fg_a)).astype(np.uint8)


def draw_obj(frame, obj, p1c, p2c, dx, dy, da, scale):
    # 描繪物件
    cv.line(frame, (int(round(p1c[0])), int(round(p1c[1]))),
            (int(p2c[0]), int(p2c[1])), (0x00, 0x00, 0xFF), 2)
    fc = get_cp(frame)
    pc = ((p1c[0] + p2c[0]) / 2 + dx, (p1c[1] + p2c[1]) / 2 + dy)
    pcd = ((p1c[0] - p2c[0]), (p1c[1] - p2c[1]))
    tan = pcd[1] / pcd[0] if pcd[0] != 0 else np.inf
    angle = -(np.arctan(tan) / np.pi * 180 + da)
    if abs(angle) > 90:
        angle += 180 * (-1 if angle >= 0 else 1)
    obj = scale_image(obj, fc, scale)
    obj = move_image(obj, pc[0] - fc[0], pc[1] - fc[1])
    obj = rotate_image(obj, pc, angle)
    return blend_image(obj, frame), pc, angle


haarcascades_path = find_haarcascades_path()
face_cascade = read_haarcascade(haarcascades_path, 'frontalface_default')
eye_cascade = read_haarcascade(haarcascades_path, 'eye')
nose_cascade = read_haarcascade(haarcascades_path, 'mcs_nose')
mouth_cascade = read_haarcascade(haarcascades_path, 'mcs_mouth')

cap = cv.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError('unable to open the camera')
sw = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
sh = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
hat = read_obj('hat.png', sw, sh)
mst = read_obj('mustache.png', sw, sh)

while True:
    ok, frame = cap.read()
    if not ok:
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = detect_scales(gray, face_cascade)
    for (fx, fy, fw, fh) in faces:
        gray_face = gray[fy:fy+fh, fx:fx+fw]
        fhh = fh // 2
        gray_face_u = gray_face[0:fhh, :]
        gray_face_d = gray_face[fhh:fh, :]
        eyes = detect_scales(gray_face_u, eye_cascade)
        if len(eyes) >= 2:
            e1x, e1y, e1w, e1h = eyes[0]
            e2x, e2y, e2w, e2h = eyes[1]
            e1c = add_pair((fx + e1x, fy + e1y), get_cp(e1w, e1h))
            e2c = add_pair((fx + e2x, fy + e2y), get_cp(e2w, e2h))
            scale = fw / 600
            dx = fw * -0.16
            dy = (e1y + (e1h - 1) / 2 + e2y + (e2h - 1) / 2) * -0.8
            frame, pc, angle = draw_obj(frame, hat, e1c, e2c, dx, dy, 0, scale)
            text = f'hat: pos ({pc[0]:8.4f},{pc[1]:8.4f}), '
            text += f'angle {angle: 8.4f}, scale {scale: 6.4f}'
            draw_text(frame, text, sw - 1, 0, 0.6, (0x00, 0xFF, 0x00), 2)
        noses = detect_scales(gray_face_d, nose_cascade)
        mouths = detect_scales(gray_face_d, mouth_cascade)
        if len(noses) >= 1 and len(mouths) >= 1:
            nx, ny, nw, nh = noses[0]
            mx, my, mw, mh = mouths[0]
            nc = add_pair((fx + nx, fy + fhh + ny), get_cp(nw, nh))
            mc = add_pair((fx + mx, fy + fhh + my), get_cp(mw, mh))
            scale = fw / 960
            dy = fw * 0.03
            frame, pc, angle = draw_obj(frame, mst, nc, mc, 0, dy, 90, scale)
            text = f'mst: pos ({pc[0]:8.4f},{pc[1]:8.4f}), '
            text += f'angle {angle: 8.4f}, scale {scale: 6.4f}'
            draw_text(frame, text, sw - 1, 16, 0.6, (0x00, 0xFF, 0x00), 2)
        cv.rectangle(frame, (fx, fy), (fx + fw - 1, fy + fh - 1),
                     (0xFF, 0x00, 0x00), 1)
    cv.imshow('frame', frame)
    if cv.waitKey(1) >= 0:
        break

cap.release()
cv.destroyAllWindows()
