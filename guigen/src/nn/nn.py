import json
import os

from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor


class NeuralNetwork(object):
    def __init__(self, training_dir):
        training_files = map(
            lambda fn: os.path.join(training_dir, fn),
            filter(
                lambda fn: os.path.isfile(os.path.join(training_dir, fn)),
                os.listdir(training_dir),
            ),
        )

        # training_data = []
        self.training_inputs = []
        self.training_outputs = []

        for f in training_files:
            data = NeuralNetwork.read_training_data(f)
            self.training_inputs.extend(data[0])
            self.training_outputs.extend(data[1])

        # print(training_data)
        # self.training_inputs = [data[0] for data in training_data]
        # print(self.training_inputs)
        # self.training_outputs = [data[1] for data in training_data]
        # print(self.training_outputs)
        self.dim = len(self.training_inputs[0])
        # print(self.dim)

        self.model = Sequential()
        self.model.add(Dense(self.dim + 8, input_dim=self.dim, activation="relu"))
        self.model.add(Dense(1, kernel_initializer="normal"))
        self.model.compile(
            loss="mean_squared_error", optimizer="adam", metrics=["accuracy"]
        )

    def fit(self):
        self.model.fit(
            self.training_inputs,
            self.training_outputs,
            epochs=150,
            batch_size=10,
            verbose=False,
        )
        _, accuracy = self.model.evaluate(self.training_inputs, self.training_outputs)
        return accuracy

    def predict(self, input_data):
        # print(input_data)
        return self.model.predict([input_data,])[
            0
        ][0]
        # return self.model.predict(self.training_inputs)

    @staticmethod
    def read_training_data(filename):
        with open(filename, "r") as f:
            d = json.load(f)

        trials = d["Trials"]
        # print(trials)
        param_mats = []
        times = []
        for t in trials:
            buttons = t["Buttons"]
            tm = []
            for b in buttons:
                tm.extend(
                    [
                        b["x"],
                        b["y"],
                        b["width"],
                        b["height"],
                        b["colors"]["fg"]["r"],
                        b["colors"]["fg"]["g"],
                        b["colors"]["fg"]["b"],
                        b["colors"]["bg"]["r"],
                        b["colors"]["bg"]["g"],
                        b["colors"]["bg"]["b"],
                        b["shape"],
                        int(b["text"] == "Goal"),
                    ]
                )
            param_mats.append(tm)
            times.append(t["Time"])

        return (param_mats, times)
