"""
integration

Integration test suite
"""

import logging
import time
import threading
import unittest
from unittest.mock import patch, mock_open
import warnings
from src.system import System

logging.disable(logging.ERROR)

MOCK_NODE_CONFIG = """
pipe_node:
  module: pipe_node
  config:
    pipe_path: /tmp/automation.pipe
"""

MOCK_CONDITION_CONFIG = """
- pipe_conditions
"""

class TestIntegration(unittest.TestCase):
    """
    Test case class
    """

    def test_integration(self):
        """
        Checks that the node updates its state when started/stopped
        """

        warnings.simplefilter('ignore')
        with patch('builtins.open', new_callable=mock_open) as mock_file:
            mock_file.side_effect = [
                mock_open(read_data=MOCK_NODE_CONFIG).return_value,
                mock_open(read_data=MOCK_CONDITION_CONFIG).return_value
            ]

            _system = System()
            _system.start()

        time.sleep(1)

        with open('/tmp/automation.pipe', 'w') as pipe:
            pipe.write('stop')

        time.sleep(1)

        self.assertEqual(threading.active_count(), 1)
