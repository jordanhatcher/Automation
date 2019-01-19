import sys, os
sys.path.append(os.path.join(sys.path[0], '../src'))

import unittest
from unittest.mock import patch, mock_open
import config_loader as cl


class TestConfigLoader(unittest.TestCase):

    def test_valid_config(self):
        config_file_contents = """
        system:
          log_level: INFO
          time_zone: US/Eastern
        nodes:
          unix_socket_node:
            node_type: default.unix_server
            config:
              socket_path: /var/automation/automation.sock
        conditions:
          unix_server_conditions:
        """

        expected_system_config = {
            'log_level': 'INFO',
            'time_zone': 'US/Eastern'
        }

        expected_node_config = {
            'unix_socket_node': {
                'node_type': 'default.unix_server',
                'config': {
                    'socket_path': '/var/automation/automation.sock'
                }
            }
        }

        expected_condition_config = {
            'unix_server_conditions': None
        }

        with patch("builtins.open", mock_open(read_data=config_file_contents)) as mock_file:
            system_config, node_config, condition_config = cl.load_config('/tmp/')

        self.assertDictEqual(expected_system_config, system_config)
        self.assertDictEqual(expected_node_config, node_config)
        self.assertDictEqual(expected_condition_config, condition_config)

    def test_missing_nodes(self):
        config_file_contents = """
        system:
          log_level: INFO
          time_zone: US/Eastern
        conditions:
          unix_server_conditions:
        """

        expected_system_config = {
            'log_level': 'INFO',
            'time_zone': 'US/Eastern'
        }

        expected_node_config = {}

        expected_condition_config = {
            'unix_server_conditions': None
        }

        with patch("builtins.open", mock_open(read_data=config_file_contents)) as mock_file:
            system_config, node_config, condition_config = cl.load_config('/tmp/')

        self.assertDictEqual(expected_system_config, system_config)
        self.assertEqual(expected_node_config, node_config)
        self.assertDictEqual(expected_condition_config, condition_config)

    def test_missing_conditions(self):
        config_file_contents = """
        system:
          log_level: INFO
          time_zone: US/Eastern
        nodes:
          unix_socket_node:
            node_type: default.unix_server
            config:
              socket_path: /var/automation/automation.sock
        """

        expected_system_config = {
            'log_level': 'INFO',
            'time_zone': 'US/Eastern'
        }

        expected_node_config = {
            'unix_socket_node': {
                'node_type': 'default.unix_server',
                'config': {
                    'socket_path': '/var/automation/automation.sock'
                }
            }
        }

        expected_condition_config = {}

        with patch("builtins.open", mock_open(read_data=config_file_contents)) as mock_file:
            system_config, node_config, condition_config = cl.load_config('/tmp/')

        self.assertDictEqual(expected_system_config, system_config)
        self.assertDictEqual(expected_node_config, node_config)
        self.assertEqual(expected_condition_config, condition_config)


    def test_missing_system(self):
        config_file_contents = """
        nodes:
          unix_socket_node:
            node_type: default.unix_server
            config:
              socket_path: /var/automation/automation.sock
        """

        expected_system_config = {}

        expected_node_config = {
            'unix_socket_node': {
                'node_type': 'default.unix_server',
                'config': {
                    'socket_path': '/var/automation/automation.sock'
                }
            }
        }

        expected_condition_config = {}

        with patch("builtins.open", mock_open(read_data=config_file_contents)) as mock_file:
            system_config, node_config, condition_config = cl.load_config('/tmp/')

        self.assertDictEqual(expected_system_config, system_config)
        self.assertDictEqual(expected_node_config, node_config)
        self.assertEqual(expected_condition_config, condition_config)
