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

    @property
    def subject(self) -> str:
        return self.__subject

    @subject.setter
    def subject(self, sub):
        self.__subject = sub

    @property
    def course(self) -> str:
        return self.__course

    @course.setter
    def course(self, crs):
        self.__course = crs

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, desc):
        self.__description = desc

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, ttl):
        self.__title = ttl

    @property
    def prerequisites(self) -> list:
        return self.__prerequisites

    @prerequisites.setter
    def prerequisites(self, pre):
        self.__prerequisites = pre

    def get_course_info(self) -> None:
        load_dotenv()
        base_uri = os.getenv('COURSE_SERVICE_URI')

        if base_uri is None:
            raise URLUndefinedException("Undefined URL")
        elif self.subject is None or self.course is None:
            raise PreconditionException("Missing Inputs")

        full_uri = "{}subject={}&number={}&term={}".format(base_uri, self.subject, self.course, "202280")
        data = None

        try:
            r = requests.get(full_uri)
            r.raise_for_status()
            data = r.json()
            if data['attribute'] is None or data is None:
                raise CourseNotFoundException("Course Not Found")
            self.subject = (data['attribute']['subject'])
            self.course = (data['attribute']['number'])
            self.title = (data['attribute']['title'])
            self.description = (data['attribute']['description'])
            self.prerequisites = (data['attribute']['prerequisites'])

        except HTTPError as ex:
            print("Error! " + str(ex))
        except ConnectionError as ce:
            print("Connection Error! " + str(ce.args[0]))
            raise ServiceUnavailableException("Service Unavailable")

    def __str__(self):
        return "{} {}\n{}\n{}\n".format(self.subject, self.course, self.title, self.description)
