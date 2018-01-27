import unittest
import warnings

from pubsub import pub
from src.state import State

class TestState(unittest.TestCase):

    def test_receive_message(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore",category=DeprecationWarning)
            def test_listener(**message):
                    self.assertEqual(message['value'], 'initial_value')
                    self.assertEqual(message['previous_value'], None)

            s = State()
            s.add_node('test_node_label')
            s.add_state('test_node_label', 'test_state_key')
            pub.subscribe(test_listener, 'state.test_node_label')
            s.update_state('test_node_label', 'test_state_key', 'initial_value')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestState)
    unittest.TextTestRunner(verbosity=2).run(suite)

