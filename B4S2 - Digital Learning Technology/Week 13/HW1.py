import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


def main():
    try:
        df_train = pd.read_csv(
            'http://archive.ics.uci.edu/ml/'
            'machine-learning-databases/adult/adult.data', header=None)
        df_test = pd.read_csv(
            'http://archive.ics.uci.edu/ml/'
            'machine-learning-databases/adult/adult.test',
            skiprows=[0], header=None)
    except:
        df_train = pd.read_csv('adult.data', header=None)
        df_test = pd.read_csv('adult.test', skiprows=[0], header=None)

    X_train = df_train[df_train != ' ?'].dropna()
    X_test = df_test[df_test != ' ?'].dropna()

    y_train = pd.DataFrame(X_train[14])
    y_test = pd.DataFrame(X_test[14])

    y_test[14] = y_test[14].astype(str).str.split('.').str[0]
    y_train[14] = y_train[14].astype(str).str.split('.').str[0]

    X_train = X_train.drop([14], axis=1)
    X_test = X_test.drop([14], axis=1)

    le = preprocessing.LabelEncoder()

    X_train['labels_1'] = le.fit_transform(X_train[1])
    X_train['labels_3'] = le.fit_transform(X_train[3])
    X_train['labels_5'] = le.fit_transform(X_train[5])
    X_train['labels_6'] = le.fit_transform(X_train[6])
    X_train['labels_7'] = le.fit_transform(X_train[7])
    X_train['labels_8'] = le.fit_transform(X_train[8])
    X_train['labels_9'] = le.fit_transform(X_train[9])
    X_train['labels_13'] = le.fit_transform(X_train[13])

    X_train_clean = X_train[[
        0, 'labels_1', 2, 'labels_3', 4, 'labels_5', 'labels_6', 'labels_7',
        'labels_8', 'labels_9', 10, 11, 12, 'labels_13']].copy()
    X_train_clean.columns = [i for i in range(14)]

    X_test['labels_1'] = le.fit_transform(X_test[1])
    X_test['labels_3'] = le.fit_transform(X_test[3])
    X_test['labels_5'] = le.fit_transform(X_test[5])
    X_test['labels_6'] = le.fit_transform(X_test[6])
    X_test['labels_7'] = le.fit_transform(X_test[7])
    X_test['labels_8'] = le.fit_transform(X_test[8])
    X_test['labels_9'] = le.fit_transform(X_test[9])
    X_test['labels_13'] = le.fit_transform(X_test[13])

    X_test_clean = X_test[[
        0, 'labels_1', 2, 'labels_3', 4, 'labels_5', 'labels_6', 'labels_7',
        'labels_8', 'labels_9', 10, 11, 12, 'labels_13']].copy()
    X_test_clean.columns = [i for i in range(14)]

    y_train['labels'] = le.fit_transform(y_train[14])
    y_test['labels'] = le.fit_transform(y_test[14])

    y_train_clean = y_train.drop([14], axis=1)
    y_test_clean = y_test.drop([14], axis=1)

    y_train_clean.apply(pd.to_numeric)
    y_test_clean.apply(pd.to_numeric)

    X_train_clean.apply(pd.to_numeric)
    X_test_clean.apply(pd.to_numeric)

    y_train_clean = np.ravel(y_train_clean)

    knn = KNeighborsClassifier(n_neighbors=2)
    knn.fit(X_train_clean, y_train_clean)
    prediction = knn.predict(X_test_clean)
    score = knn.score(X_test_clean, y_test_clean)

    output = pd.DataFrame(columns=('actual', 'prediction'))
    output['actual'] = y_test_clean['labels']
    output['prediction'] = prediction

    output.loc[output['actual'] == 0, ['actual']] = '<=50K'
    output.loc[output['actual'] == 1, ['actual']] = '>50K'
    output.loc[output['prediction'] == 0, ['prediction']] = '<=50K'
    output.loc[output['prediction'] == 1, ['prediction']] = '>50K'

    writePath = '410521209_KNN_predict.txt'
    with open(writePath, 'a') as f:
        f.write(f'testing score: {score}')
        f.write(output.to_string(header=True, index=False))


if __name__ == '__main__':
    main()
