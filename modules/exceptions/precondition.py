

class PreconditionException(Exception):
    def __init__(self, msg):
        self.message = "Precondition not met: {}".format(msg)
        super().__init__(self.message)

    def __str__(self):
        return self.message

