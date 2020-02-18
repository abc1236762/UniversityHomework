# Environment: conda create -n tf1 --strict-channel-priority \
#                    python=3.6 tensorflow-gpu=1.14 keras numpy=1.16 \
#                    pydot matplotlab opencv jupyter pylint autopep8

# Fix `unsubscriptable-object` (https://github.com/PyCQA/pylint/issues/3139)
# pylint: disable=E1136

# Fix `utils.plot_model` (https://github.com/keras-team/keras/issues/10638)
# in ~/miniconda3/envs/tf1/lib/python3.6/site-packages/keras/utils/vis_utils.py
# change `    layers = model.layers` to `    layers = model._layers` at line 64

import glob
import logging
import os
from os import path
from typing import List

import cv2 as cv
import numpy as np
from keras import activations, callbacks, layers
from keras import losses, models, optimizers, utils
from matplotlib import pyplot as plt

# 屏蔽Tensorflow產生的額外輸出，例如偵錯用訊息、警告。
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.FATAL)


# 資料集的路徑、訓練和驗證用的資料的資料夾、標籤表
DATASET_PATHS = glob.glob('dataset/**/*.jpg', recursive=True)
TRAIN_DATA_DIRS = [f'dataset/Set{i}' for i in range(1, 4)]
TEST_DATA_DIRS = [f'dataset/Set{i}' for i in range(4, 6)]
LABEL_TABLE = {f'{i:04}': i // 3 for i in range(0, 9)}


# 讀取資料
def read_data(data_dirs: List[str]) -> (np.ndarray, np.ndarray):
    # 取得所有資料的路徑
    data_paths = [x for x in DATASET_PATHS if any(y in x for y in data_dirs)]
    data_paths.sort()
    x, y = [], []
    # 對於所有資料，讀取資料的圖片內容和其標籤（答案）
    for data_path in data_paths:
        x.append(cv.imread(data_path, cv.IMREAD_GRAYSCALE) / 255.0)
        y.append(LABEL_TABLE[path.normpath(data_path).split(path.sep)[2]])
    x, y = np.array(x), utils.to_categorical(y)
    return x.reshape(x.shape + (1,)), y


# 讀取整個資料集
def read_dataset() -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray):
    # 讀取訓練用的資料
    x_train, y_train = read_data(TRAIN_DATA_DIRS)
    # 讀取驗證用的資料
    x_test, y_test = read_data(TEST_DATA_DIRS)
    assert x_train.shape[1:] == x_test.shape[1:]
    assert y_train.shape[1:] == y_test.shape[1:]
    return x_train, y_train, x_test, y_test


# 建立模型
def make_model(input_shape: int, num_classes: int) -> models.Sequential:
    model = models.Sequential([
        # 第一層卷積層
        layers.Conv2D(32, kernel_size=(3, 3), input_shape=input_shape),
        layers.BatchNormalization(),
        layers.Activation(activations.relu),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dropout(0.4),
        # 第二層卷積層
        layers.Conv2D(64, kernel_size=(3, 3)),
        layers.BatchNormalization(),
        layers.Activation(activations.relu),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dropout(0.4),
        # 第三層卷積層
        # layers.Conv2D(96, kernel_size=(3, 3)),
        # layers.BatchNormalization(),
        # layers.Activation(activations.relu),
        # layers.MaxPooling2D(pool_size=(2, 2)),
        # layers.Dropout(0.4),
        # 輸出層
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.4),
        layers.Dense(num_classes, activation='softmax'),
    ])
    model.compile(optimizer=optimizers.Nadam(),
                  loss=losses.categorical_crossentropy,
                  metrics=['accuracy'])
    return model


# 儲存圖表
def save_plot(dir_name: str, history: callbacks.History, label: str):
    plt.figure(figsize=(8, 4))
    plt.plot(history.history[label])
    plt.plot(history.history['val_' + label])
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig(path.join(dir_name, f'{label}.png'), bbox_inches='tight')


# 儲存結果
def save_result(dir_name: str, model: models.Sequential,
                history: callbacks.History):
    os.makedirs(dir_name)
    # 儲存模型結構
    utils.plot_model(model, to_file=path.join(dir_name, 'model.png'),
                     show_shapes=True, show_layer_names=False)
    # 儲存模型
    model.save(path.join(dir_name, 'model.hdf5'))
    # 儲存所有圖表
    save_plot(dir_name, history, 'acc')
    save_plot(dir_name, history, 'loss')


# 主程式
def main():
    # 讀取資料集
    x_train, y_train, x_test, y_test = read_dataset()
    # 指定輸入大小等等，批次大小為訓練資料數量的一半
    input_shape, num_classes = x_train.shape[1:], y_train.shape[1]
    batch_size, epochs = x_train.shape[0] // 2, 128
    # 建立和訓練模型
    model = make_model(input_shape, num_classes)
    model.summary()
    history = model.fit(x_train, y_train,
                        batch_size=batch_size,
                        epochs=epochs,
                        verbose=2,
                        validation_data=(x_test, y_test))
    # 顯示並儲存結果
    score = model.evaluate(x_test, y_test, verbose=0)
    print(f'Test loss: {score[0]}, Test accuracy: {score[1]}', )
    dir_name = path.join('results', f'loss-{score[0]:.4f}_acc-{score[1]:.4f}')
    save_result(dir_name, model, history)


if __name__ == '__main__':
    main()
