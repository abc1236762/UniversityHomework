from typing import Any, Dict, List, Optional, Type

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import ParameterGrid
from sklearn.naive_bayes import BernoulliNB, ComplementNB
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier


def read_dataset() -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray):
    # 讀取csv檔，並從每個儲存非數字欄位中的所有值做成內容不重複的列表
    df = pd.read_csv('toy_dataset.csv', index_col='Number')
    cities = list(df['City'].unique())
    genders = list(df['Gender'].unique())
    illnesses = list(df['Illness'].unique())

    def add_data(x: List[List[int]], y: List[List[int]], s: pd.Series):
        # 將每一筆資料加入陣列，並將非數字的值以內容不重複之列表的索引值替換
        x.append([cities.index(s['City']),
                  genders.index(s['Gender']),
                  s['Age'], s['Income']])
        y.append(illnesses.index(s['Illness']))

    x_train, y_train, x_test, y_test = [], [], [], []
    # 前130000筆資料作為訓練用，其他作為測試用
    for i in range(0, 130000):
        add_data(x_train, y_train, df.iloc[i])
    for i in range(130000, 150000):
        add_data(x_test, y_test, df.iloc[i])
    # 轉成資料型態為float64的numpy陣列後回傳
    return (np.array(x_train, dtype=np.float64),
            np.array(y_train, dtype=np.float64),
            np.array(x_test, dtype=np.float64),
            np.array(y_test, dtype=np.float64))


def find_best_clf(clf_class: Type[Any], param_grid: ParameterGrid,
                  x_train: np.ndarray, y_train: np.ndarray,
                  x_test: np.ndarray, y_test: np.ndarray) -> (
                      Any, Dict[str, Any]):
    best_clf, best_params, best_test_acc = None, {}, 0
    # 對於參數表格中每種參數組合做疊代
    for params in param_grid:
        # 建立包含當前參數的分類器並訓練
        clf = clf_class(**params)
        clf.fit(x_train, y_train)
        # 取得用測試資料算出的正確率，如果高於當前最高的，就換掉
        test_acc = clf.score(x_test, y_test)
        if test_acc > best_test_acc:
            best_clf, best_params, best_test_acc = clf, params, test_acc
    # 回傳最好的分類器的其參數
    return best_clf, best_params


def print_result(clf: Any, x_train: np.ndarray, y_train: np.ndarray,
                 x_test: np.ndarray, y_test: np.ndarray,
                 best_params: Optional[Dict[str, Any]] = None):
    # 如果需要輸出最好的參數則輸出，並輸出用訓練和測試資料算出的正確率
    if best_params is not None:
        print(f'- best params:    {best_params}')
    print(f'- train accuracy: {clf.score(x_train, y_train):.6f}')
    print(f'- test accuracy:  {clf.score(x_test, y_test):.6f}')


def hw1(x_train: np.ndarray, y_train: np.ndarray,
        x_test: np.ndarray, y_test: np.ndarray):
    print('Decision tree classifier')
    # 設置好決策樹分類器的參數表格
    param_grid = ParameterGrid({'criterion': ['gini', 'entropy'],
                                'splitter': ['best', 'random'],
                                'max_depth': [10, 15, 20, None],
                                'min_samples_split': [2, 3, 4],
                                'min_samples_leaf': [1, 2, 3]})
    # 針對上述參數表格的所有組合進行決策樹分類器的訓練，取得成果最好的分類器並輸出結果
    clf, best_params = find_best_clf(
        DecisionTreeClassifier, param_grid, x_train, y_train, x_test, y_test)
    print_result(clf, x_train, y_train, x_test, y_test, best_params)


def hw2(x_train: np.ndarray, y_train: np.ndarray,
        x_test: np.ndarray, y_test: np.ndarray):
    # 先將資料進行標準化，每一欄的範圍縮成0至1
    scaler = MinMaxScaler()
    scaler.fit(np.concatenate((x_train, x_test)))
    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)

    def train_nb(name: str, nb_class: Type[Any]):
        print(f'{name} naive Bayes classifier')
        # 建立單純貝氏分類器並訓練，然後輸出結果
        clf = nb_class()
        clf.fit(x_train, y_train)
        print_result(clf, x_train, y_train, x_test, y_test)

    # 訓練各種單純貝氏分類器
    train_nb('Bernoulli', BernoulliNB)
    train_nb('Complement', ComplementNB)
    train_nb('Gaussian', GaussianNB)
    train_nb('Multinomial', MultinomialNB)

    print('K-nearest neighbors classifier')
    # 設置好KNN分類器的參數表格
    param_grid = ParameterGrid({'n_neighbors': [4, 5, 6],
                                'weights': ['uniform', 'distance'],
                                'algorithm': ['ball_tree', 'kd_tree', 'brute'],
                                'leaf_size': [20, 30, 40],
                                'p': [1, 2]})
    # 針對上述參數表格的所有組合進行KNN分類器的訓練，取得成果最好的分類器並輸出結果
    clf, best_params = find_best_clf(
        KNeighborsClassifier, param_grid, x_train, y_train, x_test, y_test)
    print_result(clf, x_train, y_train, x_test, y_test, best_params)


if __name__ == '__main__':
    # 先設置隨機數的種子，以方便重現結果
    np.random.seed(0)
    # 讀取資料集，分成訓練和測試用
    x_train, y_train, x_test, y_test = read_dataset()
    # 作業1
    hw1(x_train, y_train, x_test, y_test)
    # 作業2
    hw2(x_train, y_train, x_test, y_test)
