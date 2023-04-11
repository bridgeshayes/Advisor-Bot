

class URLUndefinedException(Exception):
    def __init__(self, msg):
        self.message = "Url undefined: check settings in .env: {}".format(msg)
        super().__init__(self.message)

    def __str__(self):
        return self.message

