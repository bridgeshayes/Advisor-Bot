import os
from unittest import TestCase
from dotenv import load_dotenv
from train import load_classifier
from modules.contexts.context import Context
import modules.states.conversation as conversation
import modules.states.conversation.course as course



class TestBusiness(TestCase):
    def setUp(self) -> None:
        if load_dotenv():
            CLASSIFICATION_MODEL = os.getenv('CLASSIFICATION_MODEL')
        self.classifier = load_classifier(CLASSIFICATION_MODEL=CLASSIFICATION_MODEL, channel_name="advisor")
        self.context = Context("Default", self.classifier)
        self.context.state = conversation.Business("Business", self.context)

    def test_small_talk(self):
        next_state = self.context.state.parse_response("Hello")
        self.assertIsInstance(next_state, conversation.Business)

    def test_business(self):
        next_state = self.context.state.parse_response("I need schedule information")
        self.assertIsInstance(next_state, conversation.Business)

    def test_restart(self):
        next_state = self.context.state.parse_response("Cheers for that")
        self.assertIsInstance(next_state, conversation.Initiation)

    def test_yeet(self):
        next_state = self.context.state.parse_response("quit")
        self.assertIsInstance(next_state, conversation.Feedback)

    def test_course(self):
        next_state = self.context.state.parse_response("I need course information")
        self.assertIsInstance(next_state, course.QueryCourse)
