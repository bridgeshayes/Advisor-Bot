from modules.common.state import State
import modules.states.conversation as conversation
import modules.states.conversation.course as course
import modules.contexts as contexts
import modules.states.conversation.directory as directory


class Feedback(State):

    def parse_response(self, user_msg: str) -> "State":
        intent_class, response = self.classify_response(user_msg)
        self.message = response
        # self.message = intent_class + ": " + response
        if intent_class in self.restart_states:
            next_state = conversation.Initiation("Initiation", self.context)
        elif intent_class in self.smalltalk_states:
            next_state = conversation.Preview("Preview", self.context)
        elif intent_class == "yeet":
            next_state = conversation.Closing("Closing", self.context)
        elif intent_class in self.intent_states:
            if intent_class == "course_info":
                child_context = contexts.CourseContext("Course", self.context.classifier)
                next_state = course.QueryCourse("Subject_Course", self.context, child_context)
                self.message = "What is the subject and course (ex. CSC 2310)?"
            elif intent_class == "directory_info":
                child_context = contexts.DirectoryContext("Directory", self.context.classifier)
                next_state = directory.QueryDirectory("Directory", self.context, child_context)
                self.message = "What is the name of the person you are looking for?"
            else:
                next_state = conversation.Preview("Preview", self.context)
        else:
            next_state = self
        return next_state
