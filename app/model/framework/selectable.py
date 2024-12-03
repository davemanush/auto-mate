class Selectable:
    def __init__(self):
        self.selected = False

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def is_selected(self):
        return self.selected

