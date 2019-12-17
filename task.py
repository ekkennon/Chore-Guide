class Task:
    # Task is an instance of a chore
    def __init__(self, name, num, date, mins, difficulty, necessity, fun, classification, notes):
        self.name = name
        self.num = num
        self.date = date
        self.mins = mins
        self.difficulty = difficulty
        self.necessity = necessity
        self.fun = fun
        self.classification = classification
        self.notes = notes

    def to_list(self):
        return [[self.name, self.num, self.date, self.mins, self.difficulty, self.necessity, self.fun,
                 self.classification, self.notes]]
