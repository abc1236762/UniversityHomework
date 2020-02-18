import abc

import numpy as np

from layers import Layer
from losses import Loss
from optimizers import Optimizer


class Model(metaclass=abc.ABCMeta):
    '''模型類別的抽象類別，制定模型類別應具備的屬性和函數。'''

    # 定義訓練函式的樣式，包含需要輸入batch size、epochs等。
    @abc.abstractmethod
    def train(self, x: np.ndarray, y: np.ndarray, batch_size: int,
              epochs: int, verbose_step: int = 1) -> np.ndarray:
        pass


class Sequential(Model):
    '''實做Sequential模型的類別。'''

    def __init__(self, layers: [Layer], input_dim: int,
                 optimizer: Optimizer, loss: Loss):
        # 初始化時，需要輸入所有的層物件的列表、輸入的維度、優化器和損失函數物件。
        self.layers = layers
        self.input_dim = input_dim
        self.optimizer = optimizer
        self.loss = loss
        # 因為有了輸入維度，因此可以開始對所有的層做建構。
        self.__build_layers()

    # 會對所有的層做建構的私有函式。
    def __build_layers(self):
        # 對第一層的層代入輸入的維度進行建構，剩下的層的輸入維度接續上一層的輸出維度進行。
        input_dim = self.input_dim
        for layer in self.layers:
            layer.build(input_dim)
            input_dim = layer.units

    # 對所有的層進行forward的私有函式。
    def __forward_layers(self, x: np.ndarray) -> np.ndarray:
        y_pred = x
        for layer in self.layers:
            y_pred = layer.forward(y_pred)
        return y_pred

    # 對所有的層進行backward的私有函式。
    def __backward_layers(self, grad_y: np.ndarray) -> np.ndarray:
        grad_x = grad_y
        for layer in reversed(self.layers):
            grad_x = layer.backward(grad_x)
        return grad_x

    # 計算損失的函式。
    def __calc_loss(self, y_true: np.ndarray, y_pred: np.ndarray):
        loss_val = self.loss.forward(y_true, y_pred)
        grad_y = self.loss.backward(1)
        return loss_val, grad_y

    # 進行訓練的函式。
    def train(self, x: np.ndarray, y: np.ndarray, batch_size: int,
              epochs: int, verbose_step: int = 1) -> np.ndarray:
        assert verbose_step > 0
        # 清除優化器中暫存的參數、初始化空的陣列來存預測結果和每個epoch的損失值。
        self.optimizer.clear()
        y_pred = np.empty(y.shape)
        losses = np.empty(epochs)
        # 對每個epoch進行疊代，正式開始訓練。
        for epoch in range(epochs):
            # 先針對batch size對資料進行切割。
            data_begin = batch_size * epoch
            data_range = range(data_begin, data_begin + batch_size)
            x_slice = x.take(data_range, mode='wrap', axis=0)
            y_slice = y.take(data_range, mode='wrap', axis=0)
            # 將切割資後的資料進行forward，並將結果塞入存預測結果的陣列中。
            y_slice_pred = self.__forward_layers(x_slice)
            y_pred.put(data_range, y_slice_pred, mode='wrap')
            # 計算損失，並接回backward。
            losses[epoch], grad_y = self.__calc_loss(y_slice, y_slice_pred)
            _grad_x = self.__backward_layers(grad_y)
            # 對每一層的層代入優化器進行參數的優化。
            for i in range(len(self.layers)):
                self.layers[i].optimize(i, self.optimizer)
            # 如果epoch已經滿足verbose step的倍數，輸出當前epoch的損失值。
            if (epoch + 1) % verbose_step == 0:
                print(f'Epoch {epoch + 1:-4}: loss={losses[epoch]:.8f}')
        # 訓練結束後回傳預測結果和所有損失值。
        return y_pred, losses
