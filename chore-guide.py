""" resume module 4 (about One Hot Encoding), maybe transform minutes spent to be divided by 5 """


import csv
import chart
import ai
from goal import Goal
from chore import Chore
from task import Task
from datetime import datetime


def main():
    stay = True
    while stay:
        print("0 - add a completed task\n",
              "1 - run the AI\n",
              "2 - create a new Task/Chore type\n",
              "3 - create a new Goal type\n",
              "4 - visualize data\n",
              "5 - exit\n")
        item = int(input("select option: "))

        if item == 0:
            get_task_data()
        elif item == 1:
            ai.runai(taskFile)
        elif item == 2:
            add_chore()
        elif item == 3:
            add_goal()
        elif item == 4:
            visualize()
        elif item == 5:
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
    cat = input("enter the category (NeedMotivate, NeedLimit, NeedReminder, NeedFinish): ")  # get int instead

    task = Task(chore, num, curr_date, timespent, drate, nrate, frate, cat, note)
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


curr_date = datetime.today().date()
taskFile = "taskData.csv"
choreFile = "choreTypes.csv"
goalFile = "goalTypes.csv"
goalList = get_list_from_file(goalFile, "GoalName")
choreList = get_list_from_file(choreFile, "ChoreName")
todaysTasks = get_task_by("Date", curr_date)
print(todaysTasks)
main()
