class Ownable:
    def __init__(self, owner, parent):
        self.owner = owner
        self.parent = parent

    def get_parent(self):
        return self.owner

    def update_parent(self, owner):
        self.owner = owner

    def get_owner(self):
        return self.owner

    def update_owner(self, owner):
        self.owner = owner

