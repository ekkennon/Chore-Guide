class Goal:
    def __init__(self, name, priority, notes):
        self.name = name
        self.priority = priority
        self.notes = notes

    def to_list(self):
        return [[self.name, self.priority, self.notes]]

    def get_priority(self):
        return self.priority

    def get_notes(self):
        return self.notes
