import abc
from typing import Any, Dict, List, Tuple

import numpy as np


class Optimizer(metaclass=abc.ABCMeta):
    '''優化器類別的抽象類別，制定優化器類別應具備的屬性和函數。'''

    # 定義清除優化器中暫存的參數的函式的樣式。
    @abc.abstractmethod
    def clear(self) -> float:
        pass

    # 定義更新代入優化器中的參數的函式的樣式。
    @abc.abstractmethod
    def update(self, ident: int, param: np.ndarray, grad: np.ndarray) -> float:
        pass


class GradientDescent(Optimizer):
    '''實做GD優化器的類別。'''

    def __init__(self, learning_rate: float = 0.01, momentum: float = 0.0):
        self.learning_rate = learning_rate
        self.momentum = momentum
        # 初始化時，建立一張用來存每個參數個別對應的velocity的表，
        # 因為每個參數代入優化器的識別碼不一定連續，所以建字典而不是用列表。
        self.velocities: Dict[int, np.ndarray] = dict()

    # 清除優化器中所有的velocity。
    def clear(self) -> float:
        self.velocities.clear()

    # 更新代入優化器中的參數的函式。
    def update(self, ident: int, param: np.ndarray, grad: np.ndarray) -> float:
        assert param.shape == grad.shape
        # 如果當前代入的參數沒有優化過，先給他一個全為0的velocity。
        if ident not in self.velocities:
            self.velocities[ident] = np.zeros(param.shape)
        # v' = m * v - lr * g
        self.velocities[ident] = \
            self.momentum * self.velocities[ident] - self.learning_rate * grad
        # p' = p + v'
        param = param + self.velocities[ident]
        return param
