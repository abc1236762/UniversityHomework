import numpy as np
import pandas as pd
import os

from sklearn.svm import SVC
from sklearn import tree
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def plot_decision_regions(x, y, classifier, test_idx=None, resolution=0.02):

    # setup marker generator and color map
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    # plot the decision surface
    x1_min, x1_max = x[:, 0].min() - 1, x[:, 0].max() + 1
    x2_min, x2_max = x[:, 1].min() - 1, x[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.3, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=x[y == cl, 0],
                    y=x[y == cl, 1],
                    alpha=0.8,
                    c=colors[idx],
                    marker=markers[idx],
                    label=cl,
                    edgecolor='black')

    # highlight test examples
    if test_idx:
        # plot all examples
        x_test, y_test = x[test_idx, :], y[test_idx]

        plt.scatter(x_test[:, 0],
                    x_test[:, 1],
                    c='',
                    edgecolor='black',
                    alpha=1.0,
                    linewidth=1,
                    marker='o',
                    s=100,
                    label='test set')


def get_wine_dataset(feature_1=5, feature_2=13, test_rate=0.3):
    df = pd.read_csv("wine/wine.data", header=None)
    y = df.iloc[:130, 0].values
    y = np.where(y == 1, -1, 1)
    x = df.iloc[:130, [feature_1, feature_2]].values
    return int(x.shape[0]*test_rate), train_test_split(x, y, test_size=test_rate, random_state=1, stratify=y)


def tree_classifier(method, **params):
    model = method(**params)
    plot_decision_regions(params['x_combined'], params['y_combined'],
                          classifier=model,
                          test_idx=range(130-params['test_size'], 103))
    plt.xlabel('petal length [cm]')
    plt.ylabel('petal width [cm]')
    plt.title(method.__name__)
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(f'images/{method.__name__}.png', dpi=300)
    # plt.show()


def decision_tree(x_train, y_train, x_combined, y_combined, test_size):
    tree_model = tree.DecisionTreeClassifier(
        criterion='gini', max_depth=15, random_state=1)
    tree_model.fit(x_train, y_train)
    model = tree_model
    return model


def random_forest(x_train, y_train, x_combined, y_combined, test_size):
    forest = RandomForestClassifier(
        criterion='entropy', n_estimators=22, random_state=1, n_jobs=4)
    forest.fit(x_train, y_train)

    return forest


def KNN(x_train_std, y_train, x_combined_std, y_combined, test_size):
    knn = KNeighborsClassifier(n_neighbors=5, p=2, metric='minkowski')
    knn.fit(x_train_std, y_train)
    plot_decision_regions(x_combined_std, y_combined,
                          classifier=knn, test_idx=range(130-test_size, 130))
    plt.xlabel('petal length [standardized]')
    plt.ylabel('petal width [standardized]')
    plt.legend(loc='upper left')
    plt.title('KNN')
    plt.tight_layout()
    plt.savefig('images/KNN.png', dpi=300)
    # plt.show()


def SVM(x_train_std, y_train, x_combined_std, y_combined, test_size, **params):
    svm = SVC(**params)
    svm.fit(x_train_std, y_train)

    plot_decision_regions(x_combined_std,
                          y_combined,
                          classifier=svm,
                          test_idx=range(130-test_size, 130))
    title = 'Kernel SVM' if params['kernel'] == 'rbf' else 'SVM'

    plt.xlabel('petal length [standardized]')
    plt.ylabel('petal width [standardized]')
    plt.legend(loc='upper left')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(f'images/{title}.png', dpi=300)
    # plt.show()


def main():
    test_size, (x_train, x_test, y_train, y_test) = get_wine_dataset()

    sc = StandardScaler()
    sc.fit(x_train)
    x_train_std = sc.transform(x_train)
    x_test_std = sc.transform(x_test)

    x_combined = np.vstack((x_train, x_test))
    y_combined = np.hstack((y_train, y_test))
    x_combined_std = np.vstack((x_train_std, x_test_std))

    SVM(x_train_std, y_train, x_combined_std, y_combined, test_size,
        kernel='linear', C=100.0, random_state=1)

    SVM(x_train_std, y_train, x_combined_std, y_combined, test_size,
        kernel='rbf', random_state=1, gamma=256, C=100.0)
    # exit()
    tree_classifier(decision_tree, x_train=x_train, y_train=y_train,
                    x_combined=x_combined, y_combined=y_combined, test_size=test_size)

    tree_classifier(random_forest, x_train=x_train, y_train=y_train,
                    x_combined=x_combined, y_combined=y_combined, test_size=test_size)

    KNN(x_train_std, y_train, x_combined_std, y_combined, test_size)


if __name__ == "__main__":
    if not os.path.isdir('images'):
        os.mkdir('images')
    main()
