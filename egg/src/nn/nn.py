import json
import os

from ga.structures import UIRepr

from keras.models import Sequential
from keras.layers import Dense, BatchNormalization
from keras.wrappers.scikit_learn import KerasRegressor

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

from nn import settings


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

        self.model = self.baseline_model()

        # self.estimators = []
        # self.estimators.append(("standardize", StandardScaler()))
        # self.estimators.append(
        #     (
        #         "mlp",
        #         KerasRegressor(
        #             build_fn=self.baseline_model,
        #             epochs=settings.EPOCHS,
        #             batch_size=settings.BATCH_SIZE,
        #             verbose=settings.VERBOSE,
        #         ),
        #     )
        # )
        # self.pipeline = Pipeline(self.estimators)
        # self.estimator = KerasRegressor(
        #     build_fn=self.baseline_model,
        #     epochs=settings.EPOCHS,
        #     batch_size=settings.BATCH_SIZE,
        #     verbose=settings.VERBOSE,
        # )

        # kfold = KFold(n_splits=10)
        # results = cross_val_score(
        #     self.estimator, self.training_inputs, self.training_outputs, cv=kfold
        # )
        # print("Standardized: %.2f (%.2f) MSE" % (results.mean(), results.std()))

    def baseline_model(self):
        model = Sequential()
        model.add(Dense(self.dim + 8, input_dim=self.dim, activation="relu"))
        model.add(Dense(1, kernel_initializer="normal"))
        model.compile(loss="mean_squared_error", optimizer="adam", metrics=["accuracy"])
        return model

    def fit(self):
        self.model.fit(
            self.training_inputs,
            self.training_outputs,
            epochs=settings.EPOCHS,
            batch_size=settings.BATCH_SIZE,
            verbose=settings.VERBOSE,
        )
        _, accuracy = self.model.evaluate(self.training_inputs, self.training_outputs)
        return accuracy

    def predict(self, input_data):
        # print(input_data)
        preds = self.model.predict(input_data)
        return [p[0] for p in preds]
        # return self.model.predict(input_data).values()
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
            param_mats.append(UIRepr(*tm).normalize())
            times.append(t["Time"])
        # print(param_mats)
        return (param_mats, times)
