"""
test_pipe_node

Test suite for pipe_node.py
"""

import unittest
import warnings
import time

from pubsub import pub
from src.state import State
from src.nodes.pipe_node import PipeNode

class TestPipeNode(unittest.TestCase):
    """
    Test case class
    """

    def test_update_state(self):
        """
        Checks that the node updates its state when started/stopped
        """

        warnings.simplefilter('ignore')
        def test_listener(msg):
            """
            Runs assertions on the received message
            """

            self.assertIsNotNone(msg)

        pub.subscribe(test_listener, 'state.pipe_node')
        pub.subscribe(test_listener, 'messages.pipe_node')

        _state = State()
        _pipe_node = PipeNode('pipe_node', _state,
                              config={'pipe_path': '/tmp/automation.pipe'})
        pub.sendMessage('system.node.pipe_node.start')
        time.sleep(1)
        pub.sendMessage('system.node.pipe_node.stop')
        _pipe_node.join()
