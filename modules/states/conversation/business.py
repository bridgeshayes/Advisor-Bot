from modules.common.state import State
import modules.states.conversation as conversation
import modules.states.conversation.course as course
import modules.contexts as contexts


class Business(State):

    def parse_response(self, user_msg: str) -> "State":
        intent_class, response = self.classify_response(user_msg)
        # self.message = intent_class + ": " + response
        self.message = response
        if intent_class in self.restart_states:
            next_state = conversation.Initiation("Initiation", self.context)
        elif intent_class == "yeet":
            next_state = conversation.Feedback("Feedback", self.context)
        else:
            if intent_class == "course_info":
                self.message = "What is the subject and course (ex. CSC 2310)?"
                child_context = contexts.CourseContext("Course", self.context.classifier)
                next_state = course.QueryCourse("Subject_Course", self.context, child_context)
            else:
                next_state = self
        return next_state
