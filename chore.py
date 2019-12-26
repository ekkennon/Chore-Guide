class Chore:
    def __init__(self, name, goal, mins, necessity, difficulty, fun, category, priority, notes):
        self.name = name
        self.goal = goal
        self.mins = mins
        self.necessity = necessity
        self.difficulty = difficulty
        self.fun = fun
        self.category = category
        self.priority = priority
        self.notes = notes

    def to_list(self):
        return [[self.name, self.goal, self.mins, self.necessity, self.difficulty, self.fun, self.category,
                 self.priority, self.notes]]

    def get_mins(self):
        return self.mins

    def get_necessity(self):
        return self.necessity

    def get_difficulty(self):
        return self.difficulty

    def get_fun(self):
        return self.fun

    def get_category(self):
        return self.category

    def get_priority(self):
        return self.priority

    def get_notes(self):
        return self.notes
