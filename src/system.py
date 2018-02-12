"""
system

The system module contains the system class
"""

import importlib
import logging
import os
import yaml
from pubsub import pub
from .state import State

FORMAT = '[%(asctime)s] %(levelname)s - %(name)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

LOGGER = logging.getLogger(__name__)

NODE_CONFIG_FILE_NAME = 'node_config.yml'
CONDITION_CONFIG_FILE_NAME = 'condition_config.yml'
LOCAL_DIR = os.path.dirname(__file__)

class System():
    """
    System


    """

    def __init__(self):
        """
        Constructor
        """

        self.state = State()
        self.nodes = {}
        self.conditions = {}

        pub.subscribe(self.stop, 'system.stop')
        pub.subscribe(self.restart, 'system.restart')

        LOGGER.debug('Initialized System')

    def start(self):
        """
        Starts the automation system
        """

        LOGGER.info('Starting')

        self.load_nodes()
        self.load_conditions()

        LOGGER.debug('System nodes: %s', self.nodes)
        LOGGER.debug('System conditions: %s', self.conditions)

        for node_label in self.nodes:
            LOGGER.debug('starting node %s', node_label)
            pub.sendMessage('system.node.{}.start'.format(node_label))

    def stop(self):
        """
        Stops the automation system
        """

        LOGGER.info('Stopping')

        for node_label in self.nodes:
            LOGGER.debug('stopping node %s', node_label)
            pub.sendMessage('system.node.{}.stop'.format(node_label))

    def restart(self):
        """
        Restarts the automation system
        """

        LOGGER.info('Restarting')
        self.stop()
        self.start()
        LOGGER.info('Restarted')

    def load_nodes(self):
        """
        Loads nodes based on configuration in 'node_config.yml
        """

        self.nodes = {}
        config_path = os.path.join(LOCAL_DIR, NODE_CONFIG_FILE_NAME)
        with open(config_path, 'r') as node_config_file:
            try:
                nodes = yaml.load(node_config_file)
                for label, node_contents in nodes.items():
                    LOGGER.debug('Loading node %s', label)
                    module_name = '.nodes.{}'.format(node_contents['module'])
                    module = importlib.import_module(module_name, __package__)
                    node_class = getattr(module, module.NODE_CLASS_NAME)
                    new_node = node_class(label, self.state, node_contents['config'])
                    self.nodes[label] = new_node
            except yaml.YAMLError as error:
                LOGGER.error('Unable to read node_config.yml: %s', error)

    def load_conditions(self):
        """
        Loads conditions based on configuration in 'condition_config.yml'
        """

        self.conditions = {}
        config_path = os.path.join(LOCAL_DIR, CONDITION_CONFIG_FILE_NAME)
        with open(config_path, 'r') as condition_config_file:
            try:
                conditions = yaml.load(condition_config_file)
                for condition in conditions:
                    LOGGER.debug('Loading condition %s', condition)
                    module_name = '.conditions.{}'.format(condition)
                    module = importlib.import_module(module_name, __package__)
                    new_condition = getattr(module, module.CONDITION_CLASS_NAME)()
                    self.conditions[condition] = new_condition
            except yaml.YAMLError as error:
                LOGGER.error('Unable to read condition_config.yml: %s', error)
