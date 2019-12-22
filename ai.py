import pandas
import numpy
import sklearn
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing


cat_cols = ["TaskName", "Category"]
num_cols = ["TimeSpentMins", "DifficultyRate", "NecessityRate", "FunRate"]
taskFile = "taskData.csv"
tasks = pandas.read_csv(taskFile)


def runai(task_file):
    numNeighbs = 5

    encoder = preprocessing.LabelEncoder()
    codes = encoder.fit_transform(list(tasks["Category"]))
    ohe = preprocessing.OneHotEncoder()
    encoded = ohe.fit_transform(codes.reshape(-1, 1)).toarray()

    """ scale TimeSpentMins to be more like the range of the ratings columns """
    features = list(zip(tasks["TimeSpentMins"], tasks["DifficultyRate"], tasks["NecessityRate"], tasks["FunRate"]))
    labels = list(codes)
    feature_train, feature_test, label_train, label_test = sklearn.model_selection.train_test_split(features, labels, test_size=0.01)

    model = KNeighborsClassifier(n_neighbors=numNeighbs)
    model.fit(feature_train, label_train)
    acc = model.score(feature_test, label_test)

    predicted = model.predict(feature_test)

    for i in range(len(predicted)):
        actualNeighbours = model.kneighbors([feature_test[i]], numNeighbs, True)
        # if codes[predicted[i]] != codes[label_test[i]]:
        print("Predicted: ", encoder.inverse_transform(codes[predicted[i]].reshape(1)), " (", codes[predicted[i]], ") on ",
              feature_test[i], encoder.inverse_transform(codes[label_test[i]].reshape(1)), " (", codes[label_test[i]], ")")
        # print("     Neighbours: ", numNeighbs, actualNeighbours)

    print("Accuracy: ", acc)
    return
