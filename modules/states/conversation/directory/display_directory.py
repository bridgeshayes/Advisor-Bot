from modules.common.state import State
import modules.states.conversation as conversation
import modules.contexts as contexts
import modules.states.conversation.directory as directory
from modules.exceptions import DirectoryNotFoundException, ServiceUnavailableException, PreconditionException


class DisplayDirectory(State):
    def __init__(self, name: str, parent: contexts.Context, context: contexts.CourseContext) -> None:
        super().__init__(name, context)
        self.__parent = parent
        try:
            self.context.get_directory_info()
            tmp = str(self.context)
            self.message = (tmp[:1960] + '...\n' + "Can you narrow that down?") if len(tmp) > 1960 else tmp
        except DirectoryNotFoundException as ex:
            self.message = ex.message
        except ServiceUnavailableException as ex:
            """This will never happen"""
            self.message = ex.message
        except PreconditionException as ex:
            """This will never happen"""
            self.message = ex.message

    @property
    def parent(self):
        return self.__parent

    def parse_response(self, user_msg: str) -> "State":
        intent_class, response = self.classify_response(user_msg)
        if intent_class == "contact_information":
            self.message = "Who are you looking for?"
            next_state = directory.QueryDirectory("Directory", self.parent, self.context)
        else:
            self.message = response
            next_state = conversation.Feedback("Feedback", self.parent)
        return next_state
