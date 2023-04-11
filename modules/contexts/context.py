from modules.common.state import State
from discord import Member
from modules.classifiers.common.intentclassifier import IntentClassifier


class Context(object):
    def __init__(self, name: str, classifier: IntentClassifier):
        self.__name: str = name
        self.__state: State = None
        self.__classifier: IntentClassifier = classifier

    @property
    def classifier(self) -> IntentClassifier:
        return self.__classifier

    @property
    def name(self):
        return self.__name

    @property
    def state(self) -> State:
        return self.__state

    @state.setter
    def state(self, state: State):
        """
        Same as changeState from design pattern
        :param state:
        :return:
        """
        self.__state = state

    @property
    def message(self) -> str:
        return self.__state.message

    def parse_response(self, message: str) -> State:
        return self.__state.parse_response(message)

