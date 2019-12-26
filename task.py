class Task:
    # Task is an instance of a chore
    def __init__(self, idx, name, num, date, mins, difficulty, necessity, fun, classification, priority, notes):
        self.id = idx
        self.name = name
        self.num = num
        self.date = date
        self.mins = mins
        self.difficulty = difficulty
        self.necessity = necessity
        self.fun = fun
        self.classification = classification
        self.priority = priority
        self.notes = notes

    def to_list(self):
        return [[self.id, self.name, self.num, self.date, self.mins, self.difficulty, self.necessity, self.fun,
                 self.classification, self.priority, self.notes]]
