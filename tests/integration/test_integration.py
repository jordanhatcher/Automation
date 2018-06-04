"""
integration

Integration test suite
"""

import logging
import time
import threading
import unittest
from unittest.mock import patch, mock_open
from src.system.system import System

logging.disable(logging.ERROR)

MOCK_CONFIG = """
system:
  influxdb:
    host: localhost
    port: 8086
    db_name: test

nodes:
  pipe_node:
    node: pipe_node
    config:
      pipe_path: /tmp/automation.pipe

conditions:
  pipe_conditions:
"""

class TestIntegration(unittest.TestCase):
    """
    Test case class
    """

    def test_integration(self):
        """
        Checks that the node updates its state when started/stopped
        """

        patcher = patch('builtins.open', new_callable=mock_open, read_data=MOCK_CONFIG)
        patcher.start()
        _system = System()
        patcher.stop()

        _system.start()

        time.sleep(5)
        with open('/tmp/automation.pipe', 'w') as pipe:
            pipe.write('stop')
        time.sleep(1)

        self.assertEqual(threading.active_count(), 1)
