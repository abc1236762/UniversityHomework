# Environment:
#   conda create -n tf1 --strict-channel-priority -y \
#         python=3.6 tensorflow-gpu=1.14 keras numpy=1.16 pandas \
#         matplotlib opencv pydot jupyter pylint autopep8 rope
#   conda activate tf1
#   conda config --env --set channel_priority strict
#   echo 'python 3.6.*' >> $CONDA_PREFIX/conda-meta/pinned
#   echo 'tensorflow 1.14.*' >> $CONDA_PREFIX/conda-meta/pinned
#   echo 'numpy 1.16.*' >> $CONDA_PREFIX/conda-meta/pinned
#   conda deactivate

# pylint: disable=no-member

import itertools
import logging
import os
from typing import Dict, List, Tuple

import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.layers import CuDNNLSTM, Dense
from keras.losses import mean_squared_error
from keras.models import Sequential
from keras.optimizers import Nadam
from matplotlib import pyplot as plt

# 屏蔽Tensorflow產生的額外輸出，例如偵錯用訊息、警告
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.FATAL)


# 修復使用`keras.layers.CuDNNLSTM`時會發生錯誤的問題
def fix_cudnn_lstm_issue():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    tf.Session(config=config)


# 讀取訓練資料
def read_data() -> np.ndarray:
    lines = open('train_data.txt').readlines()
    return np.array([[np.float32(x.strip())] for x in lines])


# 分割訓練資料
def split_data(data: np.ndarray, m: int) -> (np.ndarray, np.ndarray):
    x, y = [], []
    for i in range(len(data) - m):
        x.append(data[i:i + m])
        y.append(data[i + m])
    return np.array(x), np.array(y)


# 建立模型
def make_model(units: int) -> Sequential:
    model = Sequential([CuDNNLSTM(units), Dense(1)])
    model.compile(optimizer=Nadam(), loss=mean_squared_error)
    return model


# 儲存顯示訓練歷史的圖表
def save_history_plot(dir_name: str, history: Dict[str, List[float]]):
    plt.figure(figsize=(18, 6))
    plt.plot(history['loss'])
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.axis([0, len(history['loss']) - 1, 0, 0.1])
    plt.title('train history')
    plt.legend(['train'], loc='upper right')
    plt.savefig(f'{dir_name}/history.png', bbox_inches='tight')
    plt.close()


# 儲存顯示訓練結果的圖表，包含預測跟推測結果
def save_results_plot(dir_name: str,
                      result: Tuple[np.ndarray, np.ndarray, int, int, int]):
    plt.figure(figsize=(18, 6))
    y_min = np.amin(result[0]) - 0.2
    y_max = np.amax(result[0]) + 0.2
    data, data_pred, data_spec, m, t, l = result
    plt.plot(data_spec)
    plt.plot(data_pred)
    plt.plot(data)
    plt.xlabel('index')
    plt.ylabel('value')
    plt.axis([0, len(data_spec) - 1, y_min, y_max])
    plt.title('result')
    plt.legend(['spec', 'pred', 'data'], loc='upper right')
    plt.axvline(m, linestyle='--')
    plt.axvline(t, linestyle='--')
    plt.axvline(l, linestyle='--')
    plt.savefig(f'{dir_name}/result.png', bbox_inches='tight')
    plt.close()


# 不依靠既有的時間序列，只靠一筆資料預測結果，並利用預測的結果再預測，進行整個時間序列的推測
def speculate(model: Sequential, last_xi: np.ndarray, s: int):
    m = len(last_xi)
    y_spec = np.empty((s, 1))
    for i in range(s):
        x = np.concatenate((last_xi, y_spec))[i:i + m]
        y_spec[i][0] = model.predict(x.reshape((1,) + x.shape))[0][0]
    return y_spec


# 儲存模型和推測結果
def save_model_and_spec(dir_name: str, model: Sequential, spec: np.ndarray):
    model.save(f'{dir_name}/model.hdf5')
    spec_path = f'{dir_name}/spec{len(spec)}.txt'
    open(spec_path, 'w').write(','.join([repr(s[0]) for s in spec]))


# 按照不同的參數進行訓練和推測
def main(data: np.ndarray, m: int, units: int, epochs: int, spec_n: int):
    # 切割訓練資料、產生模型並訓練
    x, y = split_data(data, m)
    model = make_model(units)
    history = model.fit(x, y, batch_size=m, epochs=epochs, verbose=0)
    # 預測和推測訓練資料，並得出個別的損失
    y_pred = model.predict(x)
    y_pred_loss = K.eval(mean_squared_error(y.flatten(), y_pred.flatten()))
    y_spec = speculate(model, x[0], len(y))
    y_spec_loss = K.eval(mean_squared_error(y.flatten(), y_spec.flatten()))
    print(f'm={m} units={units} epochs={epochs} - loss: '
          f'pred={y_pred_loss:.4f} spec={y_spec_loss:.4f}')
    # 如果使用推測訓練資料產生出來的結果與正確答案差太多，則直接跳過
    if y_spec_loss >= 0.2:
        return
    # 儲存結果
    dir_name = (f'results/{m}_{units}_{epochs}_{spec_n}'
                f'-{y_pred_loss:.4f}-{y_spec_loss:.4f}')
    os.makedirs(dir_name)
    spec = speculate(model, data[-m:], spec_n)
    save_model_and_spec(dir_name, model, spec)
    data_pred = np.concatenate((x[0], y_pred))
    data_spec = np.concatenate((x[0], y_spec, spec))
    result = (data, data_pred, data_spec, m, m + len(x), len(data))
    save_history_plot(dir_name, history.history)
    save_results_plot(dir_name, result)


if __name__ == '__main__':
    fix_cudnn_lstm_issue()
    # 按照不同的參數組合下去訓練，嘗試得到最佳結果的組合
    m_range = range(10, 170, 10)
    units_range = range(10, 170, 10)
    epochs_range = range(10, 50, 10)
    data = read_data()
    for args in itertools.product(m_range, units_range, epochs_range):
        main(data, *args, 500)
