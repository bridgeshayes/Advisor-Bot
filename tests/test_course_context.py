from unittest import TestCase
import os
from dotenv import load_dotenv
from train import load_classifier
from modules.contexts.context import Context
import modules.contexts as contexts
import modules.states.conversation.course as course
from modules.exceptions import CourseNotFoundException, URLUndefinedException, PreconditionException, ServiceUnavailableException


class TestCourseContext(TestCase):
    def setUp(self) -> None:
        if load_dotenv():
            CLASSIFICATION_MODEL = os.getenv('CLASSIFICATION_MODEL')
        self.classifier = load_classifier(CLASSIFICATION_MODEL=CLASSIFICATION_MODEL, channel_name="advisor")
        self.message = "What is the subject and course (ex. CSC 2310)?"
        self.context = contexts.CourseContext("Course", self.classifier)
        self.parent = Context("Default", self.classifier)
        self.context.state = course.QueryCourse("Subject_Course", self.parent, self.context)

    def test_get_course_info(self):
        """
        Happy path test for a known course
        """
        self.context.subject = "CSC"
        self.context.course = "2310"
        self.context.get_course_info()
        self.assertEqual("Object-Oriented Prgrming/Dsgn", self.context.title)

    def test_get_diff_subject(self):
        """
        Test whether it gets data from a different subject
        """
        self.context.subject = "MATH"
        self.context.course = "2010"
        self.context.get_course_info()
        self.assertEqual("Introduction to Linear Algebra", self.context.title)

    def test_bad_URI(self):
        # Before running this test, you have to modify the COURSE_SERVICE_URI variable in .env
        self.context.subject = "CSC"
        self.context.course = "2310"
        with self.assertRaises(URLUndefinedException) as ex:
            self.context.get_course_info()

    def test_get_no_course_info(self):
        """
        Tests whether the input course exists
        """
        self.context.subject = "CSC"
        self.context.course = "0000"
        with self.assertRaises(CourseNotFoundException) as ex:
            self.context.get_course_info()

    def test_no_course_exist(self):
        """
        Tests whether the input course exists
        """
        self.context.subject = "CSC"
        self.context.course = "2518"
        with self.assertRaises(CourseNotFoundException) as ex:
            self.context.get_course_info()

    def test_get_no_parameters_info(self):
        """
        Tests whether the subject and course have been specified
        """
        self.context.subject = None
        self.context.course = None
        with self.assertRaises(PreconditionException) as ex:
            self.context.get_course_info()

    def test_get_one_parameter_missing(self):
        """
        Tests whether the subject and course have been specified
        """
        self.context.subject = "CSC"
        self.context.course = None
        with self.assertRaises(PreconditionException) as ex:
            self.context.get_course_info()

    def test_get_other_parameter_missing(self):
        """
        Tests whether the subject and course have been specified
        """
        self.context.subject = None
        self.context.course = "1020"
        with self.assertRaises(PreconditionException) as ex:
            self.context.get_course_info()

    def test_network_off(self):
        """
        Tests whether a ConnectionError is handled. Make sure that
        you have disconnected the network.
        """
        self.context.subject = "CSC"
        self.context.course = "2310"
        with self.assertRaises(ServiceUnavailableException) as ex:
            self.context.get_course_info()

    def test_uri_bad(self):
        """
        Tests whether a ConnectionError is handled. Make sure that
        you have modified the URI in the .env file
        """
        self.context.subject = "CSC"
        self.context.course = "2310"
        with self.assertRaises(ServiceUnavailableException) as ex:
            self.context.get_course_info()
