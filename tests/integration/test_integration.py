"""
integration

Integration test suite
"""

import os
import logging
import time
import threading
import unittest
from src.system import System

logging.disable(logging.ERROR)

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

class TestIntegration(unittest.TestCase):
    """
    Test case class
    """

    def test_integration(self):
        """
        Checks that the node updates its state when started/stopped
        """

        node_file_path = os.path.join(CURRENT_DIR, 'node_config.yml')
        condition_file_path = os.path.join(CURRENT_DIR, 'condition_config.yml')

        _system = System(node_file_path, condition_file_path)
        _system.start()

        time.sleep(5)

        with open('/tmp/automation.pipe', 'w') as pipe:
            pipe.write('stop')

        time.sleep(1)

        self.assertEqual(threading.active_count(), 1)
