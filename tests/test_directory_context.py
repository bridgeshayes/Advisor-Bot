from unittest import TestCase
import os
from dotenv import load_dotenv
from train import load_classifier
from modules.contexts.context import Context
import modules.contexts as contexts
import modules.states.conversation.directory as directory
from modules.exceptions import PreconditionException, ServiceUnavailableException, DirectoryNotFoundException, URLUndefinedException


class TestCourseContext(TestCase):
    def setUp(self) -> None:
        if load_dotenv():
            CLASSIFICATION_MODEL = os.getenv('CLASSIFICATION_MODEL')
        self.classifier = load_classifier(CLASSIFICATION_MODEL=CLASSIFICATION_MODEL, channel_name="advisor")
        self.message = "What is the subject and course (ex. CSC 2310)?"
        self.context = contexts.DirectoryContext("Directory", self.classifier)
        self.parent = Context("Default", self.classifier)
        self.context.state = directory.QueryDirectory("Directory", self.parent, self.context)

    def test_get_directory_info(self):
        """
        Happy path test for a known contact
        """
        self.context.query = "Jerry Gannod"
        self.context.get_directory_info()
        self.assertEqual("jgannod@tntech.edu", self.context.entries[0].email)

    def test_get_info_multiple(self):
        """
        Happy path test for query with multiple entries
        """
        self.context.query = "Gannod"
        self.context.get_directory_info()
        self.assertEqual(2, len(self.context.entries))

    def test_get_info_large(self):
        """
        Happy path test for query with multiple entries
        """
        self.context.query = "Smith"
        self.context.get_directory_info()
        self.assertEqual(34, len(self.context.entries))

    def test_get_no_query(self):
        """
        Tests an empty query string
        """
        self.context.query = ""
        with self.assertRaises(DirectoryNotFoundException) as ex:
            self.context.get_directory_info()

    def test_get_no_data(self):
        """
        Tests whether the input contact
        """
        self.context.query = "asdfalks;"
        with self.assertRaises(DirectoryNotFoundException) as ex:
            self.context.get_directory_info()

    def test_get_no_parameters_info(self):
        """
        Tests whether the query has been specified
        """
        self.context.query = None
        with self.assertRaises(PreconditionException) as ex:
            self.context.get_directory_info()

    def test_network_off(self):
        """
        Tests whether a ConnectionError is handled. Make sure that
        you have disconnected the network.
        """
        self.context.query = "Gannod"
        with self.assertRaises(ServiceUnavailableException) as ex:
            self.context.get_directory_info()

    def test_uri_bad(self):
        """
        Tests whether a MissingSchema is handled. Make sure that
        you have removed/modified the DIRECTORY_SERVICE_URI variable
        in the .env file
        """
        self.context.query = "Gannod"
        with self.assertRaises(URLUndefinedException) as ex:
            self.context.get_directory_info()
