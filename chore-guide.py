""" get input, output classification """

import pandas
import sklearn
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
import csv


def main():
    menu(int(input("enter 0 to add a task, enter 1 to run the AI")))
    done = input("press any key when done")
    return


def menu(item):
    if item == 1:
        runai()
    else:
        gettask()

    return


def gettask():
    """ blank line(s) being added at end of csv file, needs to stop """

    tname = input("enter task name")
    tnum = int(input("enter task number"))  # need to track and generate this
    tdate = input("enter the date")
    timespent = int(input("enter the approximate time spent in minutes"))
    drate = int(input("enter the difficulty rating (1{easy} to 5{difficult})"))
    nrate = int(input("enter the necessity rating (1{unnecessary} to 5{necessary})"))
    frate = int(input("enter the fun rating (1{boring} to 5{fun})"))
    tc = input("enter the classification (NeedMotivate, NeedLimit, NeedReminder, NeedFinish)")  # get int instead
    tnote = input("enter notes")
    data = [[tname, tnum, tdate, timespent, drate, nrate, frate, tc, tnote]]

    myFile = open(csvFile, 'a')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(data)

    print("task added")
    return


def runai():
    data = pandas.read_csv(csvFile)
    classes = list(data["Classification"].unique())
    numNeighbs = len(classes) + 1
    """ probably don't need this method for data with many classifications or for well-defined classifications """

    """ eventually this program should not accept data with less than 2 classifications,
    which makes the next if statement unnecessary """
    if numNeighbs < 3:
        numNeighbs = 3

    if numNeighbs % 2 == 0:
        numNeighbs = numNeighbs + 1
    """ maybe there is a more efficient way to do the proceeding if statement """

    encoder = preprocessing.LabelEncoder()
    classification = encoder.fit_transform(list(data["Classification"]))

    """ scale TimeSpentMins to be more like the range of the ratings columns """
    inputs = list(zip(data["TimeSpentMins"], data["DifficultyRate"], data["NecessityRate"], data["FunRate"]))
    outputs = list(classification)
    in_train, in_test, out_train, out_test = sklearn.model_selection.train_test_split(inputs, outputs, test_size=0.01)

    model = KNeighborsClassifier(n_neighbors=numNeighbs)
    model.fit(in_train, out_train)
    acc = model.score(in_test, out_test)

    predicted = model.predict(in_test)

    for i in range(len(predicted)):
        actualNeighbours = model.kneighbors([in_test[i]], numNeighbs, True)
        if classes[predicted[i]] != classes[out_test[i]]:
            print("Predicted: ", classes[predicted[i]], " on ", in_test[i], classes[out_test[i]])
            print("     Neighbours: ", numNeighbs, actualNeighbours)

    print("Accuracy: ", acc)
    return


csvFile = "choreData.csv"
main()
