from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


class AI:
    def __init__(self, file_dicts, tasks, chores, n_rate_model, d_rate_model, f_rate_model, cat_model, neighbours=5):
        self.cat_cols = ["TaskName", "Category"]
        self.num_cols = ["TimeSpentMins", "NecessityRate", "DifficultyRate", "FunRate"]
        self.tasks = tasks
        self.chores = chores
        self.numDict = file_dicts["num"]
        self.catDict = file_dicts["cat"]
        self.taskDict = file_dicts["task"]
        self.taskNumDict = file_dicts["taskNum"]
        self.nRateModel = n_rate_model
        self.dRateModel = d_rate_model
        self.fRateModel = f_rate_model
        self.catModel = cat_model
        self.numNeighbs = neighbours

    def nrate_model_ai(self):
        taskNames = []

        labels = list(self.tasks["NecessityRate"]) + list(self.chores["Necessity"])

        for item in list(self.tasks["TaskName"]):
            taskNames.append(self.taskNumDict.get(item))
        for item in list(self.chores["ChoreName"]):
            taskNames.append(self.taskNumDict.get(item))

        timespent = list(self.tasks['TimeSpentMins']) + list(self.chores["TimeSpent"])
        priorities = list(self.tasks["Priority"]) + list(self.chores["Priority"])

        features = list(zip(timespent, priorities, taskNames))

        model = KNeighborsClassifier(n_neighbors=self.numNeighbs)
        model.fit(features, labels)
        self.nRateModel = model

        return

    def drate_model_ai(self):
        taskNames = []
        labels = list(self.tasks["DifficultyRate"]) + list(self.chores["Difficulty"])

        for item in list(self.tasks["TaskName"]):
            taskNames.append(self.taskNumDict.get(item))
        for item in list(self.chores["ChoreName"]):
            taskNames.append(self.taskNumDict.get(item))

        timespent = list(self.tasks['TimeSpentMins']) + list(self.chores["TimeSpent"])
        necessity = list(self.tasks["NecessityRate"]) + list(self.chores["Necessity"])
        priorities = list(self.tasks["Priority"]) + list(self.chores["Priority"])

        features = list(zip(timespent, necessity, priorities, taskNames))

        model = KNeighborsClassifier(n_neighbors=self.numNeighbs)
        model.fit(features, labels)
        self.dRateModel = model

        return

    def frate_model_ai(self):
        taskNames = []
        labels = list(self.tasks["FunRate"]) + list(self.chores["Fun"])

        for item in list(self.tasks["TaskName"]):
            taskNames.append(self.taskNumDict.get(item))
        for item in list(self.chores["ChoreName"]):
            taskNames.append(self.taskNumDict.get(item))

        timespent = list(self.tasks['TimeSpentMins']) + list(self.chores["TimeSpent"])
        necessity = list(self.tasks["NecessityRate"]) + list(self.chores["Necessity"])
        difficulty = list(self.tasks["DifficultyRate"]) + list(self.chores["Difficulty"])
        priorities = list(self.tasks["Priority"]) + list(self.chores["Priority"])

        features = list(zip(timespent, necessity, difficulty, priorities, taskNames))

        model = KNeighborsClassifier(n_neighbors=self.numNeighbs)
        model.fit(features, labels)
        self.fRateModel = model

        return

    def category_model_ai(self):
        # from sklearn import preprocessing
        # le_cat = preprocessing.LabelEncoder()
        # le_cat.fit(["NeedReminder", "NeedLimit", "NeedMotivate", "NeedFinish"])
        # self.tasks["Category"] = le_cat.transform(self.tasks["Category"])

        labels = []
        for item in list(self.tasks["Category"]):
            labels.append(self.numDict.get(item))
        for item in list(self.chores["ChoreName"]):
            labels.append(self.taskNumDict.get(item))

        necessity = list(self.tasks["NecessityRate"]) + list(self.chores["Necessity"])
        difficulty = list(self.tasks["DifficultyRate"]) + list(self.chores["Difficulty"])
        fun = list(self.tasks["FunRate"]) + list(self.chores["Fun"])
        features = list(zip(necessity, difficulty, fun))

        model = DecisionTreeClassifier(criterion="entropy", max_depth=4)
        model.fit(features, labels)
        self.catModel = model

        return

    def predict(self, kind, new_data):
        if kind == "category":
            return self.catModel.predict(new_data)
        elif kind == "nrate":
            return self.nRateModel.predict(new_data)
        elif kind == "drate":
            return self.dRateModel.predict(new_data)
        elif kind == "frate":
            return self.fRateModel.predict(new_data)

    """
    def score(self):
        predicted = model.predict(feature_test)

        acc = model.score(feature_test, label_test)
        fb = metrics.accuracy_score(label_test, predicted)

        print("score: ", fb)
        print("Accuracy: ", acc)
        """
