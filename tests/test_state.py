"""
test_state

Test suite for state.py
"""

import logging
import unittest
import warnings

from pubsub import pub
from src.system.state import State

logging.disable(logging.ERROR)

class TestState(unittest.TestCase):
    """
    Test case class
    """

    def test_receive_message(self):
        """
        Checks that a message is received after a state is updated
        """

        warnings.simplefilter('ignore')
        def test_listener(msg):
            """
            Runs assertions on the received message
            """

            self.assertEqual(msg['value'], 'initial_value')
            self.assertEqual(msg['previous_value'], None)

        _state = State({
            'host': 'localhost',
            'port': 8086,
            'user': 'test',
            'pass': 'test',
            'db_name': 'test'
        })

        pub.subscribe(test_listener, 'state.test_node_label')
        _state.update_state('test_node_label', {'test_state_key': 'initial_value'})

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestState)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
