class Ownable:
    def __init__(self, owner):
        self.owner = owner

    def get_owner(self):
        return self.owner

    def update_owner(self, owner):
        self.owner = owner

