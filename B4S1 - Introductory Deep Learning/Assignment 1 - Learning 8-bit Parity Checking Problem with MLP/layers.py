import abc

import numpy as np

from activations import Activation, Linear
from optimizers import Optimizer


class Layer(metaclass=abc.ABCMeta):
    '''層類別的抽象類別，制定層類別應具備的屬性和函數。'''

    # 制定一個層的參數上限為256。
    _max_params_n = 256

    def __init__(self):
        # 先將需要的屬性定義好，包含輸入和輸出和這個層有無建構好的值。
        self.x: np.ndarray = None
        self.out: np.ndarray = None
        self.grad_x: np.ndarray = None
        self.grad_out: np.ndarray = None
        self.built = False

    # 定義建構函式的樣式，在建構時需要輸入輸入維度數。
    @abc.abstractmethod
    def build(self, input_dim: int):
        pass

    # 定義forward函式的樣式。
    @abc.abstractmethod
    def forward(self, x: np.ndarray) -> np.ndarray:
        pass

    # 定義backward函式的樣式。
    @abc.abstractmethod
    def backward(self, grad_out: np.ndarray) -> np.ndarray:
        pass

    # 定義優化函式的樣式。
    @abc.abstractmethod
    def optimize(self, layer_i: int, optimizer: Optimizer):
        pass


class Dense(Layer):
    '''實做Dense層的類別。'''

    def __init__(self, units: int, activation: Activation = None):
        super().__init__()
        self.units = units
        # 如果只有Linear不需要激勵函數的話，直接設空值。
        self.activation = activation
        # 由於Linear輸入維度必須仰賴上一個層的輸出維度或是在模型類別裡定義的輸入維度決定，
        # 因此先定義只給空值，等到模型呼叫層的建構函數時再給。
        self.linear: Linear = None

    # 進行建構的函式，在Dense中進行Linear的補全。
    def build(self, input_dim: int):
        self.linear = Linear(input_dim, self.units)
        self.built = True

    # 進行forward的函式。
    def forward(self, x: np.ndarray) -> np.ndarray:
        assert self.built
        # 假設輸入的`x`為K×M矩陣。
        self.out = self.x = x
        # 先用Linear進行forward，如果激勵函數屬性不為空值的話也代入激勵函數的forward。
        # linear.forward('(K×M)') -> '(K×N)'
        self.out = self.linear.forward(self.out)
        if self.activation is not None:
            # activation.forward('(K×N)') -> '(K×N)'
            self.out = self.activation.forward(self.out)
        return self.out

    # 進行backward的函式。
    def backward(self, grad_out: np.ndarray) -> np.ndarray:
        assert self.built
        # 假設輸入的`grad_out`為K×N矩陣。
        self.grad_x = self.grad_out = grad_out
        # 如果激勵函數屬性不為空值的話先代入激勵函數的backward，再用Linear進行backward。
        if self.activation is not None:
            # activation.backward('(K×N)') -> '(K×N)'
            self.grad_x = self.activation.backward(self.grad_x)
        # linear.backward('(K×N)') -> '(K×M)'
        self.grad_x = self.linear.backward(self.grad_x)
        return self.grad_x

    # 進行優化的函式，會輸入當前的層在模型是第幾層與模型使用的優化器。
    def optimize(self, layer_i: int, optimizer: Optimizer):
        # 算出weight和bias在優化器中的識別碼後，放入優化器進行優化。
        self.linear.weight = optimizer.update(
            layer_i * Layer._max_params_n + 0,
            self.linear.weight, self.linear.grad_weight)
        self.linear.bias = optimizer.update(
            layer_i * Layer._max_params_n + 1,
            self.linear.bias, self.linear.grad_bias)
