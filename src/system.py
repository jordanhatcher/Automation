"""
system

The system module contains the system class
"""

import importlib
import os
import yaml
from pubsub import pub
from .state import State


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
        self.start()

    def start(self):
        """
        Starts the automation system
        """
        self.load_nodes()
        self.load_conditions()

    def stop(self):
        """
        Stops the automation system
        """

        for node_label in self.nodes:
            pub.sendMessage('system.node.{}.stop'.format(node_label))

    def restart(self):
        """
        Restarts the automation system
        """

        self.stop()
        self.start()

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
                    module_name = '.nodes.{}'.format(node_contents['module'])
                    module = importlib.import_module(module_name, __package__)
                    node_class = getattr(module, module.NODE_CLASS_NAME)
                    new_node = node_class(label, self.state, node_contents['config'])
                    self.nodes[label] = new_node
            except yaml.YAMLError as error:
                print(error)

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
                    module_name = '.conditions.{}'.format(condition)
                    module = importlib.import_module(module_name, __package__)
                    new_condition = getattr(module, module.CONDITION_CLASS_NAME)()
                    self.conditions[condition] = new_condition
            except yaml.YAMLError as error:
                print(error)
