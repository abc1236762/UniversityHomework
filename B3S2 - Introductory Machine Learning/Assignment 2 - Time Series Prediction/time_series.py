import os
import random
import sys

from keras import __version__ as keras_version
from keras.activations import relu
from keras.backend import set_session
from keras.callbacks import Callback
from keras.layers import Dense
from keras.losses import mean_squared_error
from keras.models import Sequential, load_model
from keras.optimizers import Adam
import numpy
import pandas
import tensorflow


class Checkpoint(Callback):
    def __init__(self, steps: int, units: int, epoch_range: range):
        super(Callback, self).__init__()
        self.steps = steps
        self.units = units
        self.epoch_start = epoch_range.start
        self.epoch_end = \
            epoch_range.stop // epoch_range.step * epoch_range.step
        self.epochs_step = epoch_range.step
    
    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        epoch += 1
        diff = epoch - self.epoch_start
        
        if (diff >= 0) and (diff % self.epochs_step == 0):
            print("steps={} units={} epochs={} => loss={:.8f}".format(
                self.steps, self.units, epoch, logs["loss"]))
            info_str = "{}-{}-{}-{:.8f}".format(
                self.steps, self.units, epoch, logs["loss"])
            model_path = os.path.join(
                "models", "model_{}.hdf5".format(info_str))
            self.model.save(model_path, overwrite=True)
        
        if epoch == self.epoch_end:
            self.model.stop_training = True


def make_reproducible():
    if tensorflow.__version__ != "1.13.1" or keras_version != "2.2.4":
        print("Version of Tensorflow and Keras must be 1.13.1 "
              "and 2.2.4 to make prediction reproducible.")
        exit(1)
    if os.environ.get("OMP_NUM_THREADS") is None or \
            os.environ["OMP_NUM_THREADS"] != "2":
        print("OMP_NUM_THREADS must be set to 2 before running "
              "the script to make prediction reproducible.")
        exit(1)
    if os.environ.get("PYTHONHASHSEED") is None or \
            os.environ["PYTHONHASHSEED"] != "0":
        print("PYTHONHASHSEED must be set to 0 before running "
              "the script to make prediction reproducible.")
        exit(1)
    
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    tensorflow.reset_default_graph()
    random.seed(0)
    numpy.random.seed(0)
    tensorflow.set_random_seed(0)
    set_session(tensorflow.Session(
        graph=tensorflow.get_default_graph(),
        config=tensorflow.ConfigProto(
            device_count={"GPU": 0},
            intra_op_parallelism_threads=1,
            inter_op_parallelism_threads=1,
        )
    ))


def get_train_data(steps: int) -> (
        numpy.ndarray, numpy.ndarray, numpy.ndarray):
    data = pandas.read_csv("train_data.csv").values.flatten()
    count = data.shape[0] - steps
    x_train, y_train = [None] * count, [0.0] * count
    for i in range(count):
        x_train[i], y_train[i] = data[i:i + steps], data[i + steps]
    return data, numpy.array(x_train), numpy.array(y_train)


def predict(steps: int, data: numpy.ndarray,
            model: Sequential) -> numpy.ndarray:
    result = [0.0] * 250
    for i in range(250):
        x_test = data[-steps:].reshape((1, steps))
        y_test = model.predict(x_test)
        data = numpy.append(data, y_test)
        result[i] = data[-1]
    return numpy.array(result)


def time_series(steps: int, units: int, epoch_range: range):
    make_reproducible()
    data, x_train, y_train = get_train_data(steps)
    
    model = Sequential([Dense(units, activation=relu, input_dim=steps),
                        Dense(1)])
    model.compile(optimizer=Adam(), loss=mean_squared_error)
    checkpoint = Checkpoint(steps, units, epoch_range)
    history = model.fit(x_train, y_train, epochs=sys.maxsize, verbose=0,
                        callbacks=[checkpoint], shuffle=False)
    losses = history.history["loss"]
    
    for epoch in epoch_range:
        loss = losses[epoch - 1]
        info_str = "{}-{}-{}-{:.8f}".format(steps, units, epoch, loss)
        model_path = os.path.join("models", "model_{}.hdf5".format(info_str))
        prediction_path = \
            os.path.join("predictions", "prediction_{}.csv".format(info_str))
        
        model = load_model(model_path)
        result = predict(steps, data, model)
        prediction = {"serial_no": numpy.arange(1, 251), "output": result}
        pandas.DataFrame(prediction).to_csv(prediction_path, index=False)


if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    os.makedirs("predictions", exist_ok=True)
    
    for _steps in range(17, 29, 1):
        for _units in range(900, 5601, 100):
            _epoch_range = range(4400, 12001, 400)
            time_series(steps=_steps, units=_units, epoch_range=_epoch_range)
