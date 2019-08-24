from os import path
from typing import List, Tuple
import math
import os
import time

import cv2
import darknet
import numpy


class Detection:
    # 紀錄偵測資訊的結構，包含在圖片上的矩形座標、中心點、標籤和辨識率。
    def __init__(self):
        self.x1, self.x2, self.y1, self.y2 = -1, -1, -1, -1
        self.cx, self.cy, self.label, self.rate = -1, -1, "", 0.0


class MarvelYoloValid:
    # 驗證訓練結果的類別，參數`need_save_to_file`為`True`時會將結果存成圖片否則直接顯示。
    def __init__(self, need_save_to_file: bool = False):
        # 指定字體和顏色。
        self.font = cv2.FONT_HERSHEY_DUPLEX
        self.text_color = (0xFF, 0x00, 0xFF)
        self.rect_color = (0xFF, 0xFF, 0x00)
        # 初始化Darknet。
        self.darknet_net, self.darknet_net_w, self.darknet_net_h = None, 0, 0
        self.darknet_meta, self.darknet_img = None, None
        self.init_darknet()
        # 開始偵測圖片。
        self.delect_imgs(need_save_to_file)

    # 初始化Darknet的函式，會讀取YOLOv3的設定、訓練好的模型權重等相關必要資料。
    def init_darknet(self):
        config_path = "marvel_cfg/yolov3-marvel.cfg"
        weight_path = "marvel_weights/yolov3-marvel_final.weights"
        meta_path = "marvel_cfg/marvel.data"
        self.darknet_net = darknet.load_net_custom(
            config_path.encode("ascii"), weight_path.encode("ascii"), 0, 1)
        self.darknet_net_w = darknet.network_width(self.darknet_net)
        self.darknet_net_h = darknet.network_height(self.darknet_net)
        self.darknet_meta = darknet.load_meta(meta_path.encode("ascii"))
        self.darknet_img = darknet.make_image(
            self.darknet_net_w, self.darknet_net_h, 3)

    # 偵測圖片的函式，會對所有列在`marvel_data/valid.list`的圖片進行辨識並顯示或儲存結果。
    def delect_imgs(self, need_save_to_file: bool = False):
        img_paths = []
        # 在`marvel_data/valid.list`取得所有需要辨識的圖片的相對路徑。
        with open("marvel_data/valid.list") as f:
            img_paths = [s.strip() for s in f.readlines()]
        # 對於每一個圖片開始進行辨識。
        for img_path in img_paths:
            # 開啟圖片
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            print("Detecting image \"{}\"…".format(img_path), end="")
            time_now = time.time()
            # 取得偵測結果並在終端機上印出耗費時間。
            detections = self.delect_img(img)
            print(" {:.6f}s".format(time.time() - time_now))
            # 在終端機上印出偵測結果並將結果繪製在圖片上。
            for d in detections:
                print("* {}: {:5.2f}%".format(d.label, d.rate * 100))
            self.draw_detections(img, detections)
            # 判斷是否將結果存成圖片，或是直接顯示出來。
            if need_save_to_file:
                # 在`marvel_validations`資料夾中以PNG格式保存。
                name = path.splitext(path.basename(img_path))[0] + ".png"
                img_path = path.join("marvel_validations", name)
                cv2.imwrite(img_path, img)
            else:
                # 顯示圖片並保持4000毫秒再進行下一次的偵測。
                cv2.imshow("image", img)
                cv2.waitKey(4000)

    # 偵測一張圖片的函式，會直接對一張圖片進行辨識，並傳回辨識結果。
    def delect_img(self, img: numpy.ndarray) -> List[Detection]:
        # 先取得圖片的原始長寬，並將圖片轉換成在Darknet進行偵測時的必要尺寸和色彩空間。
        img_h, img_w, _ = img.shape
        img = cv2.resize(img, (self.darknet_net_w, self.darknet_net_h),
                         interpolation=cv2.INTER_LINEAR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 將圖片複製進Darknet並開始偵測，取的原始偵測資料。
        darknet.copy_image_from_bytes(self.darknet_img, img.tobytes())
        detections_raw = darknet.detect_image(
            self.darknet_net, self.darknet_meta,
            self.darknet_img, thresh=0.45)
        # 將原始偵測資料進行轉換並回傳。
        return self.trans_detections(img_w, img_h, detections_raw)

    # 將原始偵測資料進行轉換的函式，讓紀載在原始資料裡的座標符合實際圖片大小而不是Darknet的。
    def trans_detections(
            self, img_w: int, img_h: int,
            detections_raw: List[Tuple[str, float, Tuple[
                float, float, float, float]]]) -> List[Detection]:
        # 初始化紀錄偵測資訊的列表。
        detections = [Detection() for _ in range(len(detections_raw))]
        # 迭代原始偵測資料的索引值。
        for i in range(len(detections_raw)):
            # 取得當前索引值的原始偵測資料和偵測資訊結構的參考。
            r, d = detections_raw[i], detections[i]
            # 轉換偵測的標籤資訊和取得辨識率。
            d.label = r[0].decode()
            d.rate = r[1]
            # 計算座標的放大倍率，並計算實際偵測到在圖片上的中心座標、長和寬。
            wr = img_w / self.darknet_net_w
            hr = img_h / self.darknet_net_h
            x, y, w, h = r[2][0] * wr, r[2][1] * hr, r[2][2] * wr, r[2][3] * hr
            # 將中心座標、長和寬轉換為矩形座標、修正有可能超出的狀況和儲存中心座標。
            d.x1, d.y1 = int(round(x - (w / 2))), int(round(y - (h / 2)))
            d.x2, d.y2 = int(round(x + (w / 2))), int(round(y + (h / 2)))
            d.x1 = 0 if d.x1 < 0 else d.x1
            d.y1 = 0 if d.y1 < 0 else d.y1
            d.x2 = img_w - 1 if d.x2 >= img_w else d.x2
            d.y2 = img_h - 1 if d.x2 >= img_h else d.y2
            d.cx, d.cy = int(round(x)), int(round(y))
        # 回傳所有轉換後的偵測資訊
        return detections

    # 在圖片上描繪偵測資訊的函式，會將每個偵測到的地方框起，並印上標籤和辨識率。
    def draw_detections(self, img: numpy.ndarray, detections: List[Detection]):
        for d in detections:
            cv2.rectangle(img, (d.x1, d.y1), (d.x2, d.y2), self.rect_color, 2)
            self.draw_text(img, "{}: {:5.2f}%".format(d.label, d.rate * 100),
                           d.cx, d.y1 + 2, 1 / 2, 1)

    # 描繪文字的函式，參數`align`可為0到8，分別可以將文字對齊指定座標的左上、中上、右上、左中
    # 、中、右中、左下、中下、右下。
    def draw_text(self, img: numpy.ndarray, text: str,
                  x: int, y: int, size: float, align: int = 0):
        # 檢查參數`align`是不是在0到8的範圍。
        if not 0 <= align < 9:
            raise OverflowError
        # 取得描繪文字所需的尺寸並計算對應不同對齊的座標。
        (text_w, text_h), base_line = \
            cv2.getTextSize(text, self.font, size, 1)
        w, h = text_w + base_line / 2, text_h + base_line
        if align % 3 == 0:
            x = int(math.floor(x + base_line / 4))
        elif align % 3 == 1:
            x = int(round(x - w / 2 + 1 / 2 + base_line / 4))
        else:
            x = int(math.ceil(x - w + 1 + base_line / 4))
        if align // 3 == 0:
            y = int(round(y + text_h + base_line / 2 - 1))
        elif align // 3 == 1:
            y = int(round(y - h / 2 + 1 / 2 + text_h + base_line / 2 - 1))
        else:
            y = int(round(y - h + 1 + text_h + base_line / 2 - 1))
        # 將文字印在圖片上。
        cv2.putText(img, text, (x, y), self.font,
                    size, self.text_color, 1, cv2.LINE_AA)


# 腳本的執行入口。
if __name__ == "__main__":
    # 先建立`marvel_validations`資料夾作為儲存結果的地方，再開始進行驗證訓練結果。
    os.makedirs("marvel_validations", exist_ok=True)
    MarvelYoloValid(False)
