class Chore:
    def __init__(self, name, goal, mins, difficulty, necessity, fun, category, priority, notes):
        self.name = name
        self.goal = goal
        self.mins = mins
        self.difficulty = difficulty
        self.necessity = necessity
        self.fun = fun
        self.category = category
        self.priority = priority
        self.notes = notes

    def to_list(self):
        return [[self.name, self.goal, self.mins, self.difficulty, self.necessity, self.fun, self.category,
                 self.priority, self.notes]]

    def get_mins(self):
        return self.mins

    def get_difficulty(self):
        return self.difficulty

    def get_necessity(self):
        return self.necessity

    def get_fun(self):
        return self.fun

    def get_category(self):
        return self.category

    def get_notes(self):
        return self.notes