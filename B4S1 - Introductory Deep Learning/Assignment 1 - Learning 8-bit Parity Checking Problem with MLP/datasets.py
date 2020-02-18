import abc
import itertools

import numpy as np


class Dataset(metaclass=abc.ABCMeta):
    '''資料集類別的抽象類別，制定資料集類別應具備的函數。'''

    # 定義用來讀取資料的函式的樣式。
    @abc.abstractmethod
    def load_data(self) -> (np.ndarray, np.ndarray):
        pass


class ParityBits(Dataset):
    '''實現同位位元資料集的類別。'''

    # 初始化時，指定位元數量，以及是否為檢查偶數位元，如果是的話則偶數個1答案為1，預設為否。
    def __init__(self, bits_n: int, is_checking_even: bool = False):
        assert bits_n > 0
        self.bits_n = bits_n
        # 宣告能夠算出正確結果的函式屬性，將位元陣列放進去，算出1的數量，並決定答案為0還是1。
        fix = 1 if is_checking_even else 0
        self.result_of = lambda x: (np.count_nonzero(x)+fix) % 2

    # 讀取資料的函式，會回傳資料集和答案。
    def load_data(self) -> (np.ndarray, np.ndarray):
        # 先使用笛卡兒積（itertools.product）產生0和1在指定長度的排列組合的陣列。
        x = np.array(list(itertools.product(range(2), repeat=self.bits_n)))
        # 對於每一筆測資，算出正確結果。
        y = np.reshape([self.result_of(bits) for bits in x], (-1, 1))
        return x, y


class AndBits(Dataset):
    '''實現位元AND資料集的類別，拿來測試用。'''

    def __init__(self, bits_n: int):
        assert bits_n > 0
        self.bits_n = bits_n
        self.result_of = lambda x: 1 if np.count_nonzero(x == 0) == 0 else 0

    def load_data(self) -> (np.ndarray, np.ndarray):
        x = np.array(list(itertools.product(range(2), repeat=self.bits_n)))
        y = np.reshape([self.result_of(bits) for bits in x], (-1, 1))
        return x, y


class OrBits(Dataset):
    '''實現位元OR資料集的類別，拿來測試用。'''

    def __init__(self, bits_n: int):
        assert bits_n > 0
        self.bits_n = bits_n
        self.result_of = lambda x: 1 if np.count_nonzero(x) > 0 else 0

    def load_data(self) -> (np.ndarray, np.ndarray):
        x = np.array(list(itertools.product(range(2), repeat=self.bits_n)))
        y = np.reshape([self.result_of(bits) for bits in x], (-1, 1))
        return x, y
