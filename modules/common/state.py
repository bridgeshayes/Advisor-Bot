# Base class for Slot
from __future__ import annotations
import abc
from typing import TYPE_CHECKING, Tuple, List

if TYPE_CHECKING:
    from modules.contexts.context import Context


class State(object):

    def __init__(self, name: str, context: Context) -> None:
        """
        Constructor
        :param name:
        :param context: Intent
        """
        self.__name = name
        self.__context = context
        self.__message = "default message"
        self.__intent_states = ["course_info", "schedule_info", "enrollment", "switch", "directory_info"]
        self.__restart_states = ["goodbye"]
        self.__smalltalk_states = ["greeting", "well-being-inquiry", "well-being-response",
                                   "inquiry-response", "thanks"]

    @property
    def name(self):
        return self.__name

    @property
    def intent_states(self) -> List[str]:
        return self.__intent_states

    @property
    def restart_states(self) -> List[str]:
        return self.__restart_states

    @property
    def smalltalk_states(self) -> List[str]:
        return self.__smalltalk_states

    @property
    def context(self):
        return self.__context

    @context.setter
    def context(self, ctx):
        """
        Same as setContext from design pattern
        :param ctx:
        :return:
        """
        self.__context = ctx

    @property
    def message(self) -> str:
        """
        Return the message to be displayed to the user after entering into this state
        """
        # return "{}: {}".format(self.name, self.__message)
        return self.__message

    @message.setter
    def message(self, msg: str) -> None:
        self.__message = msg

    @abc.abstractmethod
    def parse_response(self, response: str) -> "State":
        """
        * Classify the response using the classify_response method and determine the next state
        * Set the message attribute for display to the user
        :param response: string input from user
        :return: State
        """
        pass

    def classify_response(self, user_msg: str) -> Tuple[str, str]:
        response, intent_info = self.context.classifier.get_response(user_msg, debug=False)
        intent_class = intent_info[0]["intent"]
        return intent_class, response
