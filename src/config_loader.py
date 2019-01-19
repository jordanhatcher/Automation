"""
Helper to load configuration
"""

import os
import yaml

CONFIG_FILE_NAME = 'config.yml'

def load_config(config_dir):
    """
    Loads the 'config.yml' file
    """

    config_path = os.path.join(config_dir, CONFIG_FILE_NAME)
    with open(config_path, 'r') as config_file:
        config = yaml.load(config_file)

        system_config = config.get('system', {})
        node_config = config.get('nodes', {})
        condition_config = config.get('conditions', {})

        return (system_config, node_config, condition_config)
