"""
test_system

Test suite for system.py
"""

import logging
import unittest
from unittest.mock import patch, mock_open

from src.system.system import System
from src.system.conditions.pipe_conditions import PipeConditions
from src.system.nodes.pipe_node import PipeNode

logging.disable(logging.ERROR)

MOCK_CONFIG = """
nodes:
  pipe_node:
    node: pipe_node
    config:
      pipe_path: /tmp/automation.pipe
  test_node:
    node: pipe_node

conditions:
  pipe_conditions:
"""

class TestSystem(unittest.TestCase):
    """
    Test case class
    """

    @patch('builtins.open', new_callable=mock_open, read_data=MOCK_CONFIG)
    def test_load_nodes(self, mocked_open):
        """
        Tests that the system loads the config.yml file properly
        """

        syst = System()
        syst.load_config()
        self.assertIsInstance(syst.nodes['pipe_node'], PipeNode)
        self.assertIsInstance(syst.nodes['test_node'], PipeNode)
        self.assertIsInstance(syst.conditions['pipe_conditions'], PipeConditions)
        mocked_open.assert_called()

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestSystem)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
