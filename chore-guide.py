import csv
import chart
from goal import Goal
from chore import Chore
from task import Task
from ai import AI
from datetime import datetime


def main():
    guide.runai()
    stay = True

    while stay:
        print("\t0 - add a completed task\n",
              "\t1 - create a new Task/Chore type\n",
              "\t2 - create a new Goal type\n",
              "\t3 - visualize data\n",
              "\t4 - exit\n")
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
            stay = False

    return


def get_task_data():
    print("Do not use special characters. They can negatively impact the data.")
    print("Choose task from : ", choreList)
    chore = input("enter the associated chore: ")
    chorerow = get_item_from_file(choreFile, chore, "ChoreName")
    c = Chore(chorerow["ChoreName"], chorerow["Goal"], chorerow["TimeSpent"], chorerow["Difficulty"],
              chorerow["Necessity"], chorerow["Fun"], chorerow["Category"], chorerow["Priority"], chorerow["Notes"])

    print("Estimated Time Taken in Minutes: ", c.get_mins())
    print("Estimated Difficulty Rating: ", c.get_difficulty())
    print("Estimated Necessity Rating: ", c.get_necessity())
    print("Estimated Fun Rating: ", c.get_fun())
    print("Predicted Category: ", c.get_category())
    print("Chore Notes: ", c.get_notes(), "\n")

    num = 1  # int(input("enter task number: "))  # need to track and generate this

    timespent = int(input("enter the approximate time spent in minutes: "))
    note = input("enter notes: ")

    # predict these
    drate = int(input("enter the difficulty rating (1{easy} to 5{difficult}): "))
    nrate = int(input("enter the necessity rating (1{unnecessary} to 5{necessary}): "))
    frate = int(input("enter the fun rating (1{boring} to 5{fun}): "))

    new_task_data = [[timespent, drate, nrate, frate]]
    cat_num = guide.new_data(new_task_data)
    cat = catDict.get(cat_num[0])  # gets item[0] because a list is returned

    task = Task(num_tasks, chore, num, curr_date, timespent, drate, nrate, frate, cat, note)
    print("Please restart application to get current num_tasks.")
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
    difficulty = int(input("enter estimated difficulty rating: "))
    necessity = int(input("enter estimated necessity rating: "))
    fun = int(input("enter estimated fun rating: "))
    category = input("enter estimated category: ")
    priority = int(input("enter priority number: "))
    notes = input("enter notes: ")
    chore = Chore(name, goal, mins, difficulty, necessity, fun, category, priority, notes)

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
            chart.main_menu(item)

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
            itemslist.append(row[column])

    return itemslist


def get_task_by(column, criteria):
    itemslist = []

    myFile = open(taskFile, 'r')
    with myFile:
        reader = csv.DictReader(myFile)
        for row in reader:
            if criteria == row[column]:
                itemslist.append(row)

    return itemslist


def get_num_tasks():
    myFile = open(taskFile, 'r')
    with myFile:
        reader = csv.DictReader(myFile)
        data = list(reader)
        count = len(data)

    return count


curr_date = datetime.today().date()
taskFile = "taskData.csv"
choreFile = "choreTypes.csv"
goalFile = "goalTypes.csv"
goalList = get_list_from_file(goalFile, "GoalName")
choreList = get_list_from_file(choreFile, "ChoreName")
num_tasks = get_num_tasks()
catDict = {0: "RM", 1: "LF"}
numDict = {v: k for k, v in catDict.items()}
guide = AI(catDict, numDict)
main()
