

class DirectoryNotFoundException(Exception):
    def __init__(self, msg):
        self.message = "Directory info not found for contact: {}".format(msg)
        super().__init__(self.message)

    def __str__(self):
        return self.message

