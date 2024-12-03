

class Creatable:
    def __init__(self):
        self.new = False

    def set_newly_created(self):
        self.new = True

    def is_created(self):
        return self.new