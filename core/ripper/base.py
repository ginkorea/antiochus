class BaseRipper:

    def __init__(self):
        self.type = None
        self.ripped = None
        self.needs_cleaning = False

    def rip(self, text):
        raise NotImplementedError("rip() method must be implemented in a subclass.")

    def clean(self):
        raise NotImplementedError("clean() method must be implemented in a subclass.")

    def write(self):
        self.ripped.to_csv("output.csv", index=False)
