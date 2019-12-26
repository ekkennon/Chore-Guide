class Task:
    # Task is an instance of a chore
    def __init__(self, idx, name, num, date, mins, necessity, difficulty, fun, classification, priority, notes):
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
        self.notes = notes

    def to_list(self):
        return [[self.id, self.name, self.num, self.date, self.mins, self.necessity, self.difficulty, self.fun,
                 self.classification, self.priority, self.notes]]
