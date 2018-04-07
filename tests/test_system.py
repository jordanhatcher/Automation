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

MOCK_NODE_CONFIG = """
pipe_node:
  node: pipe_node
  config:
    pipe_path: /tmp/automation.pipe
test_node:
  node: pipe_node
"""

MOCK_CONDITION_CONFIG = """
pipe_conditions:
  schedule: '* * * * *'
"""

class TestSystem(unittest.TestCase):
    """
    Test case class
    """

    @patch('builtins.open', new_callable=mock_open, read_data=MOCK_NODE_CONFIG)
    def test_load_nodes(self, mocked_open):
        """
        Checks that nodes are loaded from the node_config.yml file
        """

        syst = System()
        syst.load_nodes()
        self.assertIsInstance(syst.nodes['pipe_node'], PipeNode)
        self.assertIsInstance(syst.nodes['test_node'], PipeNode)
        mocked_open.assert_called()

    @patch('builtins.open', new_callable=mock_open, read_data=MOCK_CONDITION_CONFIG)
    def test_load_conditions(self, mocked_open):
        """
        Checks that conditions are loaded from the condition_config.yml file
        """

        syst = System()
        syst.load_conditions()
        self.assertIsInstance(syst.conditions['pipe_conditions'], PipeConditions)
        mocked_open.assert_called()

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestSystem)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
