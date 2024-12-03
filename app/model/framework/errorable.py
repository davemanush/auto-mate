class Errorable:
    def __init__(self):
        self.validation_error = None

    def set_validation_error(self, error):
        self.validation_error = error

    def clear_error(self):
        self.validation_error = None

    def has_error(self):
        return self.validation_error is not None
