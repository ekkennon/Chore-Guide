class Task:
    # Task is an instance of a chore
    def __init__(self, idx, name, num, date, mins, necessity, difficulty, fun, classification, priority, progress, notes):
        self.id = idx
        self.name = name
        self.num = num
        self.date = date
        self.mins = mins
        self.necessity = necessity
        self.difficulty = difficulty
        self.fun = fun
        self.classification = classification
        self.priority = priority
        self.progress = progress
        self.notes = notes
        self.catlist = []
        self.namelist = []
        self.catnumlist = []
        self.tasknumlist = []

    def to_list(self):
        return [[self.id, self.name, self.num, self.date, self.mins, self.necessity, self.difficulty, self.fun,
                 self.classification, self.priority, self.progress, self.notes]]

    def add_cat(self, name):
        self.catlist.append(name)
        return

    def add_name(self, name):
        self.namelist.append(name)
        return
