from modules.common.state import State
import modules.contexts as contexts
import modules.states.conversation.directory as directory


class QueryDirectory(State):
    def __init__(self, name: str, parent: contexts.Context, context: contexts.DirectoryContext) -> None:
        super().__init__(name, context)
        self.__parent = parent

    @property
    def parent(self):
        return self.__parent

    def parse_response(self, user_msg: str) -> "State":
        self.message = "Looking for {}".format(user_msg)
        self.context.query = user_msg
        next_state = directory.DisplayDirectory("Verify directory", self.parent, self.context)
        return next_state
