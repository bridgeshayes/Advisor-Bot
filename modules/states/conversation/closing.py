from modules.common.state import State


class Closing(State):
    def parse_response(self, response: str) -> "State":
        return self
