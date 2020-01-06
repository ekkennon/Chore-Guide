import csv
import pandas
import joblib
import os
from classes import ai, chart, taskLookup
from classes.goal import Goal
from classes.chore import Chore
from classes.task import Task
from datetime import date
from datetime import timedelta
from heapq import nsmallest
from xml.etree import ElementTree
from random import sample


def main():
    stay = True
    while stay:
        print("\t0 - add a completed task\n",
              "\t1 - create a new Task/Chore type\n",
              "\t2 - create a new Goal type\n",
              "\t3 - visualize data\n",
              "\t4 - get today's tasks\n"
              "\t5 - exit\n")
        item = int(input("select option: "))

        if item == 0:
            get_task_data()
        elif item == 1:
            add_chore()
        elif item == 2:
            add_goal()
        elif item == 3:
            visualize()
        elif item == 4:
            get_tasks(7)
        elif item == 5:
            stay = False

    return


def get_task_data():
    print("Do not use special characters. They can negatively impact the data.")
    print("Choose task from : ", choreList)
    chore = input("enter the associated chore: ")
    chorerow = get_item_from_file(choreFile, chore, "ChoreName")
    c = Chore(chorerow["ChoreName"], chorerow["Goal"], chorerow["TimeSpent"], chorerow["Necessity"], chorerow["Difficulty"],
              chorerow["Fun"], chorerow["Category"], chorerow["Priority"], chorerow["Notes"])

    taskName = taskNumDict.get(chore)

    print("Estimated Time Taken in Minutes: ", c.get_mins())
    print("Chore Notes: ", c.get_notes(), "\n")

    timespent = int(input("enter the approximate time spent in minutes: "))
    note = input("enter notes: ")

    num = 1  # int(input("enter task number: "))  # need to track and generate this
    priority = c.get_priority()
    progress = round(timespent / c.get_mins(), 1)

    guide = remake_model_files()
    nrate = guide.predict("nrate", [[timespent, priority, taskName]])[0]
    drate = guide.predict("drate", [[timespent, nrate, priority, taskName]])[0]
    frate = guide.predict("frate", [[timespent, nrate, drate, priority, taskName]])[0]
    cnum = guide.predict("category", [[nrate, drate, frate]])[0]
    cat = catDict.get(cnum)

    task = Task(len(tasks), chore, num, get_date(0), timespent, nrate, drate, frate, cat, priority, progress, note)
    tasklist = task.to_list()
    add_to_file(taskFile, tasklist)

    quotes = get_quotes(cat, "general")
    quote = sample(quotes, 1)
    print(quote[0].text)
    print("task added")
    return


def add_chore():
    print("Do not use special characters. They can negatively impact the data.")
    print("Choose goal from : ", goalList)
    goal = input("enter the associated goal: ")
    goalrow = get_item_from_file(goalFile, goal, "GoalName")
    g = Goal(goalrow["GoalName"], goalrow["Priority"], goalrow["Notes"])
    print("Goal Priority: ", g.get_priority())
    print("Goal Notes: ", g.get_notes(), "\n")

    name = input("enter new Task/Chore name: ")
    mins = int(input("enter estimated minutes needed for each instance of this task: "))
    necessity = int(input("enter estimated necessity rating: "))
    difficulty = int(input("enter estimated difficulty rating: "))
    fun = int(input("enter estimated fun rating: "))
    category = input("enter estimated category: ")
    priority = int(input("enter estimated priority number: "))
    notes = input("enter notes: ")
    chore = Chore(name, goal, mins, necessity, difficulty, fun, category, priority, notes)

    chorelist = chore.to_list()
    add_to_file(choreFile, chorelist)
    choreList.append(name)
    print("chore added")

    return


def add_goal():
    print("Do not use special characters. They can negatively impact the data.")
    name = input("enter new Goal name: ")
    priority = int(input("enter priority number: "))
    notes = input("enter notes: ")
    goal = Goal(name, priority, notes)

    goallist = goal.to_list()
    add_to_file(goalFile, goallist)
    goalList.append(name)
    print("goal added")

    return


def visualize():
    stay = True
    while stay:
        print("0 - header rows\n1 - frequencies\n2 - bar\n3 - kde\n4 - kde + histogram\n5 - scatter plot\n6 - contour "
              "plot (2d density plot)\n7 - box\n8 - violin\n9 - pair-wise scatter plot\n10 - pyplot histogram "
              "(conditional)\n11 - seaborn regplot (conditional)\n12 - bar sub plot (class separation)\n13 - class "
              "imbalance\n14 - finished visualizing\n")
        item = int(input("select option: "))
        if item == 14:
            stay = False
        else:
            chart.main_menu(item, tasks)

    return


def get_tasks(days):
    # make array of relevant days
    pastWeek = []
    while days > -1:
        days = days - 1
        pastWeek.append(get_date(days))

    # get tasks completed within [pastWeek]
    taskList = get_list_from_file(taskFile, "all")
    tl = taskLookup.TaskLookup()
    listByDate = tl.get_by_date(taskList, pastWeek)

    # calculate progress for each goal and each chore type
    # variables
    dictByType = {}
    goalDict = dict.fromkeys(goalList, 0.0)
    priorityDict = {1: 5, 2: 3, 3: 1}

    for chore in choreList:
        # task progress
        chorerow = get_item_from_file(choreFile, chore, "ChoreName")
        pscore = tl.get_progress_score(tl.get_task_progress(tl.get_by_type(listByDate, chore)))
        score2 = round((pscore / len(pastWeek)) / priorityDict[int(chorerow["Priority"])], 1)
        dictByType[chore] = score2

        # goal progress
        goal = chorerow["Goal"]
        a = goalDict[goal] + score2
        goalDict[goal] = a

    # find tasks that need the most progress
    ltscores = nsmallest(1, list(dictByType.values()))
    lowest_tasks = []
    for li in dictByType:
        if dictByType[li] in ltscores:
            lowest_tasks.append(li)

    # find goals that need the most progress
    lgscores = nsmallest(3, list(goalDict.values()))
    lowest_goals = []
    for li in goalDict:
        if goalDict[li] in lgscores:
            lowest_goals.append(li)

    print("You should do ", lowest_tasks)

    # any chore type with its goal listed should definitely be included
    # for remaining spots find lowest out of remaining goals and chore types
    # if chore type is in remaining lowest those should definitely be included
    # for goals with lowest more work is needed

    return


def add_to_file(file, line):
    myFile = open(file, 'a')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(line)
    return


def get_item_from_file(file, name, column):
    line = {}
    myFile = open(file, 'r')
    with myFile:
        reader = csv.DictReader(myFile)
        for row in reader:
            if name == row[column]:
                line = row

    return line


def get_list_from_file(file, column):
    itemslist = []

    myFile = open(file, 'r')
    with myFile:
        reader = csv.DictReader(myFile)
        for row in reader:
            if column == "all":
                itemslist.append(row)
            else:
                itemslist.append(row[column])

    return itemslist


def dict_from_list(col):
    col_dict = dict.fromkeys(set(col))
    j = 0
    for k in col_dict.keys():
        col_dict[k] = j
        j = j + 1

    return col_dict


def get_date(days):
    d = date.today() - timedelta(days=days)
    d.strftime("%Y-%m-%d")
    return d


def get_quotes(style, subtype):
    tree = ElementTree.parse("data/quotes.xml").getroot()
    quote_tree = tree.find(style)
    quote_list = quote_tree.findall("./q/[@type='" + subtype + "']")
    return quote_list


def remake_model_files():
    catModelFile = "saved-models/trainedCat.mod"
    nRateModelFile = "saved-models/trainedNRate.mod"
    dRateModelFile = "saved-models/trainedDRate.mod"
    fRateModelFile = "saved-models/trainedFRate.mod"

    if os.path.exists(nRateModelFile):
        nmodel = joblib.load(open(nRateModelFile, 'rb'))
        os.remove(nRateModelFile)
    else:
        nmodel = ""
        print("n model file does not exist, please close program.")
    if os.path.exists(dRateModelFile):
        dmodel = joblib.load(open(dRateModelFile, 'rb'))
        os.remove(dRateModelFile)
    else:
        dmodel = ""
        print("d model file does not exist, please close program.")
    if os.path.exists(fRateModelFile):
        fmodel = joblib.load(open(fRateModelFile, 'rb'))
        os.remove(fRateModelFile)
    else:
        fmodel = ""
        print("f model file does not exist, please close program.")
    if os.path.exists(catModelFile):
        cmodel = joblib.load(open(catModelFile, 'rb'))
        os.remove(catModelFile)
    else:
        cmodel = ""
        print("c model file does not exist, please close program.")

    guide = ai.AI(fileDicts, tasks, nmodel, dmodel, fmodel, cmodel)
    guide.nrate_model_ai()
    guide.drate_model_ai()
    guide.frate_model_ai()
    guide.category_model_ai()
    joblib.dump(guide.nRateModel, open(nRateModelFile, 'wb'))
    joblib.dump(guide.dRateModel, open(dRateModelFile, 'wb'))
    joblib.dump(guide.fRateModel, open(fRateModelFile, 'wb'))
    joblib.dump(guide.catModel, open(catModelFile, 'wb'))

    return guide


taskFile = "data/taskData.csv"
choreFile = "data/choreTypes.csv"
goalFile = "data/goalTypes.csv"
goalList = get_list_from_file(goalFile, "GoalName")
choreList = get_list_from_file(choreFile, "ChoreName")
taskNumDict = dict_from_list(choreList)
taskNameDict = {v: k for k, v in taskNumDict.items()}
numDict = dict_from_list(get_list_from_file(taskFile, "Category"))
catDict = {v: k for k, v in numDict.items()}
fileDicts = {"task": taskNameDict, "taskNum": taskNumDict, "num": numDict, "cat": catDict}
tasks = pandas.read_csv(taskFile)
main()
