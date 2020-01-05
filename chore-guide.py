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
    os.remove(nRateModelFile)
    os.remove(dRateModelFile)
    os.remove(fRateModelFile)
    os.remove(catModelFile)
    guide.nrate_model_ai()
    guide.drate_model_ai()
    guide.frate_model_ai()
    guide.category_model_ai()
    joblib.dump(guide.nRateModel, open(nRateModelFile, 'wb'))
    joblib.dump(guide.dRateModel, open(dRateModelFile, 'wb'))
    joblib.dump(guide.fRateModel, open(fRateModelFile, 'wb'))
    joblib.dump(guide.catModel, open(catModelFile, 'wb'))

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

    num = 1  # int(input("enter task number: "))  # need to track and generate this
    priority = c.get_priority()

    timespent = int(input("enter the approximate time spent in minutes: "))
    note = input("enter notes: ")

    progress = round(timespent/c.get_mins(), 1)

    nrate = guide.predict("nrate", [[timespent, priority, taskName]])[0]
    drate = guide.predict("drate", [[timespent, nrate, priority, taskName]])[0]
    frate = guide.predict("frate", [[timespent, nrate, drate, priority, taskName]])[0]
    cnum = guide.predict("category", [[nrate, drate, frate]])[0]
    cat = catDict.get(cnum)
    task = Task(get_num_tasks(), chore, num, today, timespent, nrate, drate, frate, cat, priority, progress, note)

    quotes = get_quotes(cat, "general")
    text = sample(quotes, 1)
    print(text[0])

    tasklist = task.to_list()
    add_to_file(taskFile, tasklist)
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
    pastWeek = [today]
    while days > 0:
        days = days - 1
        pastWeek.append(get_date(days))

    # get tasks completed within [pastWeek]
    taskList = get_list_from_file(taskFile, "all")
    tl = taskLookup.TaskLookup()
    listByDate = tl.get_by_date(taskList, pastWeek)

    # calculate progress for each goal and each chore type
    # variables
    dictByType = {}
    priorityDict = {1: 5, 2: 3, 3: 1}
    goalDict = dict.fromkeys(goalList, 0.0)

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

    # while len(list(dictByType.values)) > len(set(dictByType.values)):

    # find 3 tasks that need the most progress
    ltscores = nsmallest(1, list(dictByType.values()))
    lowest_tasks = []
    for li in dictByType:
        if dictByType[li] in ltscores:
            lowest_tasks.append(li)

    # find 3 goals that need the most progress
    lgscores = nsmallest(3, list(goalDict.values()))
    lowest_goals = []
    for li in goalDict:
        if goalDict[li] in lgscores:
            lowest_goals.append(li)

    """
    # make sure only 3 tasks are in list
    removed = True
    while len(lowest_tasks) > 3 and removed is True:
        removed = False
        for i in dictByType:
            chorerow = get_item_from_file(choreFile, i, "ChoreName")
            if chorerow["Priority"] == 3 and chorerow["ChoreName"] in lowest_tasks:
                lowest_tasks.remove(chorerow["ChoreName"])
                removed = True
            elif chorerow["Priority"] == 2 and chorerow["ChoreName"] in lowest_tasks:
                lowest_tasks.remove(chorerow["ChoreName"])
                removed = True
            elif chorerow["Priority"] == 1 and chorerow["ChoreName"] in lowest_tasks:
                lowest_tasks.remove(chorerow["ChoreName"])
                removed = True
    
    # make sure only 3 goals are in list
    while len(lowest_goals) > 3:
        for i in goalDict:
            goalrow = get_item_from_file(goalFile, i, "GoalName")
            if goalrow["Priority"] == 3 and goalrow["GoalName"] in lowest_goals:
                lowest_goals.remove(goalrow["GoalName"])
            if goalrow["Priority"] == 2 and goalrow["GoalName"] in lowest_goals:
                lowest_goals.remove(goalrow["GoalName"])

    final_list = []
    while len(final_list) < 3:
        for i in lowest_tasks:
            chorerow = get_item_from_file(choreFile, i, "ChoreName")
            if chorerow["Goal"] in goalDict:
                final_list.append(chorerow["ChoreName"])
            break
    """

    print("You should do ", lowest_tasks[0])

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


def get_num_tasks():
    myFile = open(taskFile, 'r')
    with myFile:
        reader = csv.DictReader(myFile)
        data = list(reader)
        count = len(data)

    return count


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
    tree = ElementTree.parse(quoteFile).getroot()
    quote_tree = tree.find(style)
    quote_list = quote_tree.findall("./q/[@type='" + subtype + "']")
    return quote_list


today = get_date(0)
taskFile = "data/taskData.csv"
choreFile = "data/choreTypes.csv"
goalFile = "data/goalTypes.csv"
quoteFile = "data/quotes.xml"
catModelFile = "saved-models/trainedCat.mod"
nRateModelFile = "saved-models/trainedNRate.mod"
dRateModelFile = "saved-models/trainedDRate.mod"
fRateModelFile = "saved-models/trainedFRate.mod"
goalList = get_list_from_file(goalFile, "GoalName")
choreList = get_list_from_file(choreFile, "ChoreName")
nmodel = joblib.load(open(nRateModelFile, 'rb'))
dmodel = joblib.load(open(dRateModelFile, 'rb'))
fmodel = joblib.load(open(fRateModelFile, 'rb'))
cmodel = joblib.load(open(catModelFile, 'rb'))
taskNumDict = dict_from_list(choreList)
taskNameDict = {v: k for k, v in taskNumDict.items()}
numDict = dict_from_list(get_list_from_file(taskFile, "Category"))
catDict = {v: k for k, v in numDict.items()}
fileDicts = {"task": taskNameDict, "taskNum": taskNumDict, "num": numDict, "cat": catDict}
tasks = pandas.read_csv(taskFile)
guide = ai.AI(fileDicts, tasks, cmodel, nmodel, dmodel, fmodel)
main()
