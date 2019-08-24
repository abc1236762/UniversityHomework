import os
import re

from skimage.io import imread
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
import joblib
import numpy
import pandas


def read_images(dir_name: str, pattern: str) -> (numpy.ndarray, numpy.ndarray):
    image_paths = [os.path.join(dir_name, f) for f in os.listdir(dir_name)]
    pat = re.compile(pattern)
    images, infos = [None] * len(image_paths), [0] * len(image_paths)
    for i in range(len(image_paths)):
        images[i] = imread(image_paths[i], as_gray=True).flatten()
        infos[i] = int(pat.findall(image_paths[i])[0])
    return numpy.array(images), numpy.array(infos)


def face_recognition(components: int):
    x_train, y_train = read_images("train_data", r"(\d+)\(-?\d+\)\.jpg$")
    x_test, i_test = read_images("test_data", r"img(\d{4})\.jpg$")
    
    fitted_pca = PCA(n_components=components, whiten=True,
                     svd_solver="randomized", random_state=0).fit(x_train)
    x_train_pca = fitted_pca.transform(x_train)
    x_test_pca = fitted_pca.transform(x_test)
    
    svc = SVC(class_weight="balanced")
    param_grid = {"C": [1000, 5000, 10000, 50000, 100000, 500000, 1000000],
                  "gamma": [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1]}
    fitted_clf = GridSearchCV(svc, param_grid).fit(x_train_pca, y_train)
    
    c, gamma = fitted_clf.best_params_["C"], fitted_clf.best_params_["gamma"]
    score, model = fitted_clf.best_score_, fitted_clf.best_estimator_
    print("components={} C={} gamma={} => score={:.4f}".format(
        components, c, gamma, score))
    y_test = model.predict(x_test_pca)
    
    info_str = "{}-{}-{}-{:.4f}".format(components, c, gamma, score)
    model_path = os.path.join("models", "model_{}.pkl".format(info_str))
    prediction_path = \
        os.path.join("predictions", "prediction_{}.csv".format(info_str))
    joblib.dump(model, model_path)
    prediction = {"sample id": i_test, "person id": y_test}
    pandas.DataFrame(prediction).to_csv(prediction_path, index=False)


if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    os.makedirs("predictions", exist_ok=True)
    for _components in range(11, 31, 1):
        face_recognition(components=_components)
