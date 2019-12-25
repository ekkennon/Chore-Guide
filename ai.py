import pandas
import joblib
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression


catModel = "trainedCat.mod"
dRateModel = "trainedDRate.mod"
nRateModel = "trainedNRate.mod"
fRateModel = "trainedFRate.mod"


def predict(kind, new_data):
    file = ""
    if kind == "category":
        file = catModel
    elif kind == "drate":
        file = dRateModel
    elif kind == "nrate":
        file = nRateModel
    elif kind == "frate":
        file = fRateModel

    model = joblib.load(open(file, 'rb'))
    predicted_value = model.predict(new_data)
    return predicted_value


class AI:
    def __init__(self, file_dicts, tfile):
        self.cat_cols = ["TaskName", "Category"]
        self.num_cols = ["TimeSpentMins", "DifficultyRate", "NecessityRate", "FunRate"]
        self.taskFile = tfile
        self.tasks = pandas.read_csv(self.taskFile)
        self.catDict = file_dicts["cat"]
        self.numDict = file_dicts["num"]
        self.taskDict = file_dicts["task"]
        self.taskAltDict = file_dicts["taskAlt"]

    def category_model_ai(self):
        numNeighbs = 5
        labels = []
        taskNames = []

        for item in list(self.tasks["Category"]):
            labels.append(self.numDict.get(item))

        for item in list(self.tasks["TaskName"]):
            taskNames.append(self.taskDict.get(item))

        features = list(zip(self.tasks["TimeSpentMins"], self.tasks["DifficultyRate"], self.tasks["NecessityRate"], self.tasks["FunRate"], taskNames))

        model = KNeighborsClassifier(n_neighbors=numNeighbs)
        model.fit(features, labels)

        os.remove(catModel)
        joblib.dump(model, open(catModel, 'wb'))

        return

    def drate_model_ai(self):
        taskNames = []
        labels = list(self.tasks["DifficultyRate"])

        for item in list(self.tasks["TaskName"]):
            taskNames.append(self.taskDict.get(item))

        features = list(zip(self.tasks["TimeSpentMins"], taskNames))

        model = LinearRegression()
        model.fit(features, labels)

        os.remove(dRateModel)
        joblib.dump(model, open(dRateModel, 'wb'))
        return

    def nrate_model_ai(self):
        taskNames = []
        labels = list(self.tasks["NecessityRate"])

        for item in list(self.tasks["TaskName"]):
            taskNames.append(self.taskDict.get(item))

        features = list(zip(self.tasks["TimeSpentMins"], self.tasks["DifficultyRate"], taskNames))

        model = LinearRegression()
        model.fit(features, labels)

        os.remove(nRateModel)
        joblib.dump(model, open(nRateModel, 'wb'))
        return

    def frate_model_ai(self):
        taskNames = []
        labels = list(self.tasks["FunRate"])

        for item in list(self.tasks["TaskName"]):
            taskNames.append(self.taskDict.get(item))

        features = list(zip(self.tasks["TimeSpentMins"], self.tasks["DifficultyRate"], self.tasks["NecessityRate"], taskNames))

        model = LinearRegression()
        model.fit(features, labels)

        os.remove(fRateModel)
        joblib.dump(model, open(fRateModel, 'wb'))
        return

    """
    def score(self):
        predicted = model.predict(feature_test)

        acc = model.score(feature_test, label_test)
        fb = metrics.accuracy_score(label_test, predicted)

        print("score: ", fb)
        print("Accuracy: ", acc)
        """
