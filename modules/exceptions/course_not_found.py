

class CourseNotFoundException(Exception):
    def __init__(self, msg):
        self.message = "Course Not Found: {}".format(msg)
        super().__init__(self.message)

    def __str__(self):
        return self.message

