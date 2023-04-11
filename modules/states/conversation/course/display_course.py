from modules.common.state import State
import modules.states.conversation as conversation
import modules.states.conversation.course as course
import modules.contexts as contexts
from modules.exceptions.precondition import PreconditionException
from modules.exceptions.course_not_found import CourseNotFoundException
from modules.exceptions.service_unavailable import ServiceUnavailableException


class DisplayCourse(State):

    def __init__(self, name: str, parent: contexts.Context, context: contexts.CourseContext) -> None:
        super().__init__(name, context)
        self.__parent = parent
        try:
            self.context.get_course_info()
            self.message = str(self.context)
        except PreconditionException:
            self.message = "There was a problem with the input"
        except CourseNotFoundException:
            self.message = "There is no such course: {} {}".format(self.context.subject, self.context.course)
        except ServiceUnavailableException as ex:
            self.message = ex.message

    @property
    def parent(self):
        return self.__parent

    def parse_response(self, user_msg: str) -> "State":
        intent_class, response = self. classify_response(user_msg)
        if intent_class == "thanks":
            self.message = response
            next_state = conversation.Feedback("Feedback", self.parent)
        else:
            self.message = "What is the subject and course (ex. CSC 2310)?"
            next_state = course.QueryCourse("Subject_Course", self.parent, self.context)
        return next_state
