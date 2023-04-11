

class ServiceUnavailableException(Exception):
    def __init__(self, msg):
        self.message = "Service Unavailable: {}".format(msg)
        super().__init__(self.message)

    def __str__(self):
        return self.message

