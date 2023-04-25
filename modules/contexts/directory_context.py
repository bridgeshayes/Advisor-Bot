import os
import requests
from dotenv import load_dotenv
from modules.contexts.context import Context
from requests.exceptions import HTTPError, ConnectionError
from modules.classifiers.common.intentclassifier import IntentClassifier
from modules.exceptions import URLUndefinedException, PreconditionException, ServiceUnavailableException, \
    DirectoryNotFoundException
from modules.contexts.directory_entry import DirectoryEntry


class DirectoryContext(Context):
    def __init__(self, name: str, classifier: IntentClassifier):
        super().__init__(name, classifier)
        self.__entries: list = []
        self.__query: str = None

    @property
    def entries(self) -> list:
        return self.__entries

    @entries.setter
    def entries(self, entry):
        self.__entries = entry

    @property
    def query(self) -> str:
        return self.__query

    @query.setter
    def query(self, ques):
        self.__query = ques

    def get_directory_info(self):
        load_dotenv()
        base_uri = os.getenv('DIRECTORY_SERVICE_URI')
        api_key = os.getenv('DIRECTORY_API_KEY')

        if base_uri is None:
            raise URLUndefinedException("Undefined URL")
        elif self.query is None:
            raise PreconditionException("Missing Input")
        elif self.query == "":
            raise DirectoryNotFoundException("Directory Not Found")

        full_uri = "{}apiKey={}&searchCriteria={}".format(base_uri, api_key, self.query)
        data = None
        try:
            r = requests.get(full_uri)
            r.raise_for_status()
            data = r.json()
            if len(data) == 0:
                raise DirectoryNotFoundException("Directory Not Found")
            for x in data:
                self.entries.append(DirectoryEntry(x))
        except HTTPError:
            print("Error! ")
            raise URLUndefinedException("Undefined URL")
        except ConnectionError:
            print("Connection Error!")
            raise ServiceUnavailableException("Service Unavailable")

    def __str__(self):
        full = ""
        for x in self.entries:
            full += x.__str__()
            full += "\n"
        return full
