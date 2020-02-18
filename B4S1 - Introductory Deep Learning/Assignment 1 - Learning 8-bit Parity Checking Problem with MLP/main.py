import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from activations import ReLU, Sigmoid, Tanh
from datasets import ParityBits
from layers import Dense
from losses import MeanSquaredError
from models import Sequential
from optimizers import GradientDescent


def main():
    # 先讀取資料，並建立模型。
    # 輸入的維度為一個資料的長度，因為資料量小，batch size即為資料總數。
    x, y = ParityBits(8).load_data()
    batch_size, input_dim = x.shape
    model = Sequential(
        [Dense(64, activation=ReLU()),
         Dense(32, activation=Tanh()),
         Dense(16, activation=Tanh()),
         Dense(4, activation=None),
         Dense(1, activation=Sigmoid())],
        input_dim=input_dim,
        # 使用GD為優化器，MSE為損失函式。
        optimizer=GradientDescent(learning_rate=0.01, momentum=0.0),
        loss=MeanSquaredError())
    # 設定好epochs後訓練模型，訓練完後取得預測結果和每個epoch的損失值。
    y_pred, losses = model.train(
        x, y, batch_size=batch_size, epochs=200, verbose_step=10)

    # 因為答案皆為整數0或1，因此訓練的成果為模型預測的結果取整數。
    result = np.around(y_pred).astype(int)
    # 將答案與訓練成果相減。
    diff = np.subtract(y, result)
    print(pd.DataFrame({
        # 印出表格時，須將輸入的資料的每項陣列例如`[0 0 0 0 0 0 0 0]`轉成字串，
        # 因為Pandas的DataFrame的每一項不能吃陣列。
        "Data": [np.array_str(v) for v in x],
        "Answer": y[:, 0],
        "Prediction": [f'{v:.8f}' for v in y_pred[:, 0]],
        "Result": result[:, 0],
        # 如果答案與訓練成果在相減之後為0的話代表預測正確，否則失敗。
        "Correct": [True if v == 0 else False for v in diff[:, 0]]
    }, index=np.arange(1, len(x) + 1)).to_string())
    # 輸出最後的損失值和訓練成果與答案差了幾項，並繪製每個epoch與其損失值的變化圖表。
    print(f'loss: {losses[-1]:.8f}, difference: {np.count_nonzero(diff)}')
    plt.figure(figsize=(8, 4))
    plt.plot(losses)
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.show()


if __name__ == '__main__':
    # 開始主程式之前，先固定Numpy的隨機函數的種子，確保同樣模型在每次訓練的結果一致方便重現。
    np.random.seed(9487)
    main()
