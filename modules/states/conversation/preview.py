from modules.common.state import State
import modules.states.conversation as conversation
import modules.states.conversation.course as course
import modules.states.conversation.directory as directory
import modules.contexts as contexts


class Preview(State):

    def parse_response(self, resp: str) -> "State":
        intent_class, response = self.classify_response(resp)
        # self.message = intent_class + ": " + response
        self.message = response
        if intent_class in self.intent_states:
            if intent_class == "course_info":
                child_context = contexts.CourseContext("Course", self.context.classifier)
                next_state = course.QueryCourse("Subject_Course", self.context, child_context)
                self.message = "What is the subject and course (ex. CSC 2310)?"
            elif intent_class == "directory_info":
                child_context = contexts.DirectoryContext("Directory", self.context.classifier)
                next_state = directory.QueryDirectory("Directory", self.context, child_context)
                self.message = "What is the name of the person you are looking for?"
            else:
                next_state = conversation.Business("Business", self.context)
        elif intent_class in self.restart_states:
            next_state = conversation.Initiation("Initiation", self.context)
        else:
            next_state = self
        return next_state
