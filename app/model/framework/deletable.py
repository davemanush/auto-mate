class Deletable:
    def __init__(self):
        self.deleted = False

    def delete(self):
        self.deleted = True

    def restore(self):
        self.deleted = False

    def is_deleted(self):
        return self.deleted
