"""
test_pipe_condtions

Test suite for pipe_conditions.py
"""

import unittest
import warnings

from pubsub import pub
from src.conditions.pipe_conditions import PipeConditions

class TestPipeConditions(unittest.TestCase):
    """
    Test case class
    """

    def setUp(self):
        self.called = False

    def test_triggered_by_message(self):
        """
        Checks that the condition is triggered by a message from a PipeNode
        """

        warnings.simplefilter('ignore')
        def test_listener():
            """
            Asserts that the stop command was run
            """

            self.called = True

        _pipe_conditions = PipeConditions()
        pub.subscribe(test_listener, 'system.stop')
        pub.sendMessage('messages.pipe_node', msg={'content':'stop'})
        self.assertTrue(self.called)
