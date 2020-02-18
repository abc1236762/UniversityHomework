import abc

import numpy as np


class Activation(metaclass=abc.ABCMeta):
    '''激勵函數類別的抽象類別，制定激勵函數類別應具備的屬性和函數。'''

    def __init__(self):
        # 先將需要的屬性定義好，包含輸入和輸出。
        self.x: np.ndarray = None
        self.out: np.ndarray = None
        self.grad_x: np.ndarray = None
        self.grad_out: np.ndarray = None

    # 定義forward函式的樣式。
    @abc.abstractmethod
    def forward(self, x: np.ndarray) -> np.ndarray:
        pass

    # 定義backward函式的樣式。
    @abc.abstractmethod
    def backward(self, grad_out: np.ndarray) -> np.ndarray:
        pass


class Linear(Activation):
    '''實做Linear激勵函數的類別。'''

    def __init__(self, m: int, n: int):
        assert m > 0 and n > 0
        super().__init__()
        # 使用標準隨機分布的方式產生最初的weight（M×N矩陣）和bias（1×N矩陣）。
        self.weight = np.random.randn(m, n)
        self.bias = np.random.randn(1, n)
        self.grad_weight = np.zeros((m, n))
        self.grad_bias = np.zeros((1, n))

    # 進行forward的函式。
    def forward(self, x: np.ndarray) -> np.ndarray:
        # 假設輸入的`x`為K×M矩陣。
        self.x = x
        # 'x (K×M)' · 'weight (M×N)' -> '(K×N)'
        # '(K×N)' + 'bias (1×N)' -> 'out (K×N)'
        self.out = np.dot(self.x, self.weight) + self.bias
        return self.out

    # 進行backward的函式。
    def backward(self, grad_out: np.ndarray) -> np.ndarray:
        assert self.x is not None
        # 假設輸入的`grad_out`為K×N矩陣。
        self.grad_out = grad_out
        # 'x.T (M×K)' · 'grad_out (K×N)' -> 'grad_weight (M×N)'
        self.grad_weight = np.dot(self.x.T, self.grad_out)
        # ∑_(i=1)^(K)['grad_out (K×N)'] -> 'grad_bias (1×N)'
        self.grad_bias = np.reshape(np.sum(self.grad_out, axis=0), (1, -1))
        # 'grad_out (K×N)' · 'weight.T (N×M)' -> 'grad_x (K×M)'
        self.grad_x = np.dot(self.grad_out, self.weight.T)
        return self.grad_x


class ReLU(Activation):
    '''實做ReLU激勵函數的類別。'''

    def __init__(self):
        super().__init__()
        self.are_neg: np.ndarray = None

    # 進行forward的函式。
    def forward(self, x: np.ndarray):
        # 假設輸入的`x`為K×N矩陣。
        self.x = x
        # 紀錄輸入的矩陣裡面有哪一些值是負數的。
        self.are_neg = (self.x < 0)
        # 將輸入的矩陣中所有的負數改成0後輸出，也為K×N矩陣。
        self.out = self.x
        self.out[self.are_neg] = 0
        return self.out

    # 進行backward的函式。
    def backward(self, grad_out: np.ndarray):
        assert self.are_neg is not None
        # 假設輸入的`grad_out`為K×N矩陣。
        self.grad_out = grad_out
        # 使用在forward時記錄好哪些是負數的地方，
        # 將這輸入的矩陣的相同位置也改成0並輸出，也為K×N矩陣。
        self.grad_x = self.grad_out
        self.grad_x[self.are_neg] = 0
        return self.grad_x


class Sigmoid(Activation):
    '''實做Sigmoid激勵函數的類別。'''

    # Sigmoid(x) = 1 / (1 + e^(-x))
    @staticmethod
    def __sigmoid(x: np.ndarray) -> np.ndarray:
        return 1 / (1 + np.exp(-x))

    # Sigmoid'(x) = Sigmoid(x) * (1 - Sigmoid(x))
    @staticmethod
    def __sigmoid_grad(x: np.ndarray) -> np.ndarray:
        return Sigmoid.__sigmoid(x) * (1.0 - Sigmoid.__sigmoid(x))

    # 進行forward的函式。
    def forward(self, x: np.ndarray):
        # 假設輸入的`x`為K×N矩陣。
        self.x = x
        # Sigmoid('x (K×N)') -> 'out (K×N)'
        self.out = Sigmoid.__sigmoid(self.x)
        return self.out

    # 進行backward的函式。
    def backward(self, grad_out: np.ndarray):
        assert self.x is not None
        # 假設輸入的`grad_out`為K×N矩陣。
        self.grad_out = grad_out
        # 'grad_out (K×N)' * Sigmoid'('x (K×N)') -> 'grad_x (K×N)'
        self.grad_x = self.grad_out * Sigmoid.__sigmoid_grad(self.x)
        return self.grad_x


class Tanh(Activation):
    '''實做Tanh激勵函數的類別。'''

    # Tanh(x) = (e^(x) - e^(-x)) / (e^(x) + e^(-x))
    @staticmethod
    def __tanh(x: np.ndarray) -> np.ndarray:
        return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

    # Tanh'(x) = 1 - Tanh(x)^2
    @staticmethod
    def __tanh_grad(x: np.ndarray) -> np.ndarray:
        return 1 - np.square(Tanh.__tanh(x))

    # 進行forward的函式。
    def forward(self, x: np.ndarray):
        # 假設輸入的`x`為K×N矩陣。
        self.x = x
        # Tanh('x (K×N)') -> 'out (K×N)'
        self.out = Tanh.__tanh(self.x)
        return self.out

    # 進行backward的函式。
    def backward(self, grad_out: np.ndarray):
        assert self.x is not None
        # 假設輸入的`grad_out`為K×N矩陣。
        self.grad_out = grad_out
        # 'grad_out (K×N)' * Tanh'('x (K×N)') -> 'grad_x (K×N)'
        self.grad_x = self.grad_out * Tanh.__tanh_grad(self.x)
        return self.grad_x
