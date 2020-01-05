from datetime import datetime


class TaskLookup:
    def __init__(self, dformat="%Y-%m-%d"):
        self.date_format = dformat
        self.h = 0

    def get_by_date(self, tasklist, datelist):
        itemslist = []

        for row in tasklist:
            d = datetime.strptime(row["Date"], self.date_format).date()
            if d in datelist:
                itemslist.append(row)

        return itemslist

    def get_by_type(self, tasklist, chore):
        self.h = 1
        itemslist = []
        for item in tasklist:
            if item["TaskName"] == chore:
                itemslist.append(item)

        return itemslist

    def get_task_progress(self, tasklist):
        self.h = 1
        itemslist = []

        for item in tasklist:
            itemslist.append(item["Progress"])

        return itemslist

    def get_progress_score(self, progress_list):
        self.h = 1
        score = 0.0

        for p in progress_list:
            score = score + float(p)

        return score
