import pandas
import joblib
import sklearn
from sklearn.neighbors import KNeighborsClassifier


class AI:
    def __init__(self, cat_dict, num_dict):
        self.cat_cols = ["TaskName", "Category"]
        self.num_cols = ["TimeSpentMins", "DifficultyRate", "NecessityRate", "FunRate"]
        self.taskFile = "taskData.csv"
        self.tasks = pandas.read_csv(self.taskFile)
        self.modelFile = "trainedModel.mod"
        self.catDict = cat_dict
        self.numDict = num_dict

    def runai(self):
        numNeighbs = 5

        labels = []  # list(self.catDict.keys())
        categories = list(self.tasks["Category"])
        for item in categories:
            labels.append(self.numDict.get(item))

        features = list(zip(self.tasks["TimeSpentMins"], self.tasks["DifficultyRate"], self.tasks["NecessityRate"], self.tasks["FunRate"]))
        feature_train, feature_test, label_train, label_test = sklearn.model_selection.train_test_split(features, labels, test_size=0.01)

        model = KNeighborsClassifier(n_neighbors=numNeighbs)
        model.fit(feature_train, label_train)
        joblib.dump(model, open(self.modelFile, 'wb'))

        return

    def new_data(self, new_data):
        model = joblib.load(open(self.modelFile, 'rb'))
        predicted_value = model.predict(new_data)
        return predicted_value

    """
    def score(self):
        predicted = model.predict(feature_test)

        acc = model.score(feature_test, label_test)
        fb = metrics.accuracy_score(label_test, predicted)

        print("score: ", fb)
        print("Accuracy: ", acc)
        """
