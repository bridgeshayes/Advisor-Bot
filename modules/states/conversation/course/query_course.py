from modules.common.state import State
import modules.states.conversation as conversation
import modules.states.conversation.course as course
import modules.contexts as contexts


class QueryCourse(State):

    def __init__(self, name: str, parent: contexts.Context, context: contexts.CourseContext) -> None:
        super().__init__(name, context)
        self.__parent = parent

    @property
    def parent(self):
        return self.__parent

    def parse_response(self, user_msg: str) -> "State":
        # expect user_msg to be in form of subj course
        terms = user_msg.split(" ")
        if len(terms) == 2:
            self.message = "Let me look this up. subject: {}, course: {}".format(terms[0].upper(), terms[1])
            try:
                self.context.subject = str(terms[0])
                self.context.course = int(terms[1])
                next_state = course.DisplayCourse("Verify Course", self.parent, self.context)
            except ValueError:
                self.message = "You did not enter a valid course: {} {}".format(terms[0].upper(), terms[1])
                next_state = self
        else:
            intent_class, response = self.classify_response(user_msg)
            self.message = "You did not enter a valid course."
            next_state = conversation.Preview("Preview", self.parent)
        return next_state
