import itertools

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA


class AdalineMBGD(object):
    """ADAptive LInear NEuron classifier.

    Parameters
    ------------
    eta : float
      Learning rate (between 0.0 and 1.0)
    n_iter : int
      Passes over the training dataset.
    batch_size : int
      Batch size.
    shuffle : bool (default: True)
      Shuffles training data every epoch if True to prevent cycles.
    random_state : int
      Random number generator seed for random weight
      initialization.


    Attributes
    -----------
    w_ : 1d-array
      Weights after fitting.
    cost_ : list
      Sum-of-squares cost function value averaged over all
      training examples in each epoch.


    """

    def __init__(self, eta=0.01, n_iter=10, batch_size=10,
                 shuffle=True, random_state=None):
        self.eta = eta
        self.n_iter = n_iter
        self.batch_size = batch_size
        self.w_initialized = False
        self.shuffle = shuffle
        self.random_state = random_state

    def fit(self, x, y):
        """ Fit training data.

        Parameters
        ----------
        x : {array-like}, shape = [n_examples, n_features]
          Training vectors, where n_examples is the number of examples and
          n_features is the number of features.
        y : array-like, shape = [n_examples]
          Target values.

        Returns
        -------
        self : object

        """
        self._initialize_weights(x.shape[1])
        self.cost_ = []
        for i in range(self.n_iter):
            if self.shuffle:
                x, y = self._shuffle(x, y)
            count = x.shape[0]
            if count % self.batch_size != 0:
                m = count % self.batch_size
                self.batch_size += self.batch_size - m
                assert count % self.batch_size == 0
            cost = []
            for data_begin in range(0, count, self.batch_size):
                data_range = range(data_begin, data_begin + self.batch_size)
                xi = x.take(data_range, mode='wrap', axis=0)
                target = y.take(data_range, mode='wrap', axis=0)
                cost.append(self._update_weights(xi, target))
            avg_cost = sum(cost) / len(cost)
            self.cost_.append(avg_cost)
        return self

    def partial_fit(self, x, y):
        """Fit training data without reinitializing the weights"""
        if not self.w_initialized:
            self._initialize_weights(x.shape[1])
        if y.ravel().shape[0] > 1:
            for xi, target in zip(x, y):
                self._update_weights(xi, target)
        else:
            self._update_weights(x, y)
        return self

    def _shuffle(self, x, y):
        """Shuffle training data"""
        r = self.rgen.permutation(len(y))
        return x[r], y[r]

    def _initialize_weights(self, m):
        """Initialize weights to small random numbers"""
        self.rgen = np.random.RandomState(self.random_state)
        self.w_ = self.rgen.normal(loc=0.0, scale=0.01, size=1 + m)
        self.w_initialized = True

    def _update_weights(self, xi, target):
        """Apply Adaline learning rule to update the weights"""
        output = self.activation(self.net_input(xi))
        errors = target - output
        self.w_[1:] += self.eta * xi.T.dot(errors)
        self.w_[0] += self.eta * errors.sum()
        cost = (errors**2).sum()
        return cost

    def net_input(self, x):
        """Calculate net input"""
        return np.dot(x, self.w_[1:]) + self.w_[0]

    def activation(self, x):
        """Compute linear activation"""
        return x

    def predict(self, x):
        """Return class label after unit step"""
        return np.where(self.activation(self.net_input(x)) >= 0.0, 1, -1)


def read_iris_data():
    df = pd.read_csv('iris/iris.data', header=None)
    y = df.iloc[0:100, 4].values
    y = np.where(y == 'Iris-setosa', -1, 1)
    x = df.iloc[0:100, 0:4].values
    x_std = np.copy(x)
    for i in range(4):
        x_std[:, i] = (x[:, i] - x[:, i].mean()) / x[:, i].std()
    return x_std, y


def read_wine_data():
    df = pd.read_csv("wine/wine.data", header=None)
    y = df.iloc[:130, 0].values
    y = np.where(y == 1, -1, 1)
    x = df.iloc[0:130, 1:14].values
    x_std = np.copy(x)
    for i in range(13):
        x_std[:, i] = (x[:, i] - x[:, i].mean()) / x[:, i].std()
    return x_std, y


def train(x, y, method, **kwargs):
    model = method(**kwargs)
    model.fit(x, y)
    z = model.predict(x)
    score = np.sum(y == z) / x.shape[0]
    return model.cost_, score


def plot(cost):
    plt.plot(range(1, len(cost) + 1), cost, marker='o')
    plt.xlabel('Epochs')
    plt.ylabel('Average Cost')
    plt.tight_layout()
    plt.show()


def main():
    x_std, y = read_iris_data()
    cost, score = train(x=x_std, y=y, method=AdalineMBGD,
                        n_iter=8, eta=0.01, batch_size=10, random_state=1)
    print(f'iris: {score}')
    plot(cost)
    x_std, y = read_wine_data()
    cost, score = train(x=x_std, y=y, method=AdalineMBGD,
                        n_iter=8, eta=0.01, batch_size=10, random_state=1)
    print(f'wine: {score}')
    plot(cost)


if __name__ == '__main__':
    main()
