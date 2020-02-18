import abc

import numpy as np


class Loss(metaclass=abc.ABCMeta):
    '''損失函數類別的抽象類別，制定損失函數類別應具備的屬性和函數。'''

    def __init__(self):
        # 先將需要的屬性定義好，包含答案、預測和損失值的輸出等。
        self.y_true: np.ndarray = None
        self.y_pred: np.ndarray = None
        self.out = np.nan
        self.grad_y: np.ndarray = None
        self.grad_out = np.nan

    # 定義forward函式的樣式。
    @abc.abstractmethod
    def forward(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        pass

    # 定義backward函式的樣式。
    @abc.abstractmethod
    def backward(self, grad_out: float) -> np.ndarray:
        pass


class MeanSquaredError(Loss):
    '''實做MSE函數的類別。'''

    # SquaredError(y, y`) = (y - y`)^2
    @staticmethod
    def __se(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        return np.square(y_true - y_pred)

    # SquaredError'(y, y`) = -2 * (y - y`)
    @staticmethod
    def __se_grad(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        return -2 * (y_true - y_pred)

    # 進行forward的函式。
    def forward(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        self.y_true = y_true
        self.y_pred = y_pred
        # 先算出誤差的平方，再將所有誤差的平方平均後輸出。
        self.out = np.mean(MeanSquaredError.__se(self.y_true, self.y_pred))
        return self.out

    # 進行backward的函式。
    def backward(self, grad_out: float) -> np.ndarray:
        assert self.y_true is not None and self.y_pred is not None
        self.grad_out = grad_out
        # 先算出誤差的平方的grad，乘上grad out後輸出。，
        self.grad_y = self.grad_out * \
            MeanSquaredError.__se_grad(self.y_true, self.y_pred)
        return self.grad_y
