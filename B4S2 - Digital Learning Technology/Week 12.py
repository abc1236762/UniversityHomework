import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def main():
    boston = datasets.load_boston()
    x = pd.DataFrame(boston.data, columns=boston.feature_names)
    x['MEDV'] = pd.DataFrame(boston.target, columns=["MEDV"])
    table = pd.DataFrame()
    table['covariance'] = x.cov()['MEDV'].drop('MEDV')
    table['correlation coefficient'] = x.corr()['MEDV'].drop('MEDV')
    print(table)

if __name__ == '__main__':
    main()
