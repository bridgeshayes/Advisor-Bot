import os
import requests
from dotenv import load_dotenv
from modules.contexts.context import Context
from requests.exceptions import HTTPError, ConnectionError
from modules.classifiers.common.intentclassifier import IntentClassifier
from modules.exceptions import URLUndefinedException, PreconditionException, ServiceUnavailableException, DirectoryNotFoundException
from modules.contexts.directory_entry import DirectoryEntry


class DirectoryContext(Context):
    def __init__(self, name: str, classifier: IntentClassifier):
        super().__init__(name, classifier)
        self.__entries: list = []
        self.__query: str = None

    def get_directory_info(self):
        pass

    def __str__(self):
        return ""
