"""
test_state

Test suite for state.py
"""

import unittest
import warnings

from pubsub import pub
from src.state import State

class TestState(unittest.TestCase):
    """
    Test case class
    """

    def test_receive_message(self):
        """
        Checks that a message is received after a state is updated
        """

        warnings.simplefilter('ignore')
        def test_listener(**message):
            """
            Runs assertions on the received message
            """

            self.assertEqual(message['value'], 'initial_value')
            self.assertEqual(message['previous_value'], None)

        _state = State()
        _state.add_node('test_node_label')
        _state.add_states('test_node_label', ['test_state_key'])
        pub.subscribe(test_listener, 'state.test_node_label')
        _state.update_states('test_node_label', **{'test_state_key': 'initial_value'})

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestState)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
