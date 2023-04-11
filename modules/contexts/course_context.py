import os
import requests
from dotenv import load_dotenv
from modules.contexts.context import Context
from requests.exceptions import HTTPError, ConnectionError, MissingSchema
from modules.classifiers.common.intentclassifier import IntentClassifier
from modules.exceptions import URLUndefinedException, CourseNotFoundException, PreconditionException, ServiceUnavailableException


class CourseContext(Context):
    def __init__(self, name: str, classifier: IntentClassifier):
        super().__init__(name, classifier)
        self.__subject: str = None
        self.__course: str = None
        self.__description: str = None
        self.__title: str = None
        self.__prerequisites: list = []

    def get_course_info(self) -> None:
        pass

    def __str__(self):
        return ""
