"""
system

The system module contains the system class
"""

import importlib
import logging
import os
import yaml
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
from pubsub import pub
from .state import State

LOGGER = logging.getLogger(__name__)
LOCAL_DIR = os.path.dirname(__file__)
CONFIG_DIR = os.path.join(LOCAL_DIR, 'config')

MODULE_TYPES = ('conditions', 'nodes')
CLASS_NAME_CONSTS = ('NODE_CLASS_NAME', 'CONDITION_CLASS_NAME')

class System():
    """
    System

    Main system class for the automation system. It loads all config, and keeps
    references to nodes and conditions used by the system.
    """

    def __init__(self):
        """
        Constructor
        """

        self.loaded_modules = {'nodes': {}, 'conditions': {}}
        self.nodes = {}
        self.conditions = {}

        self.load_modules(LOCAL_DIR)
        self.load_packages()

        self.system_config_file = 'config.yml'
        self.system_config = None
        self.node_config = None
        self.condition_config = None

        self.load_config()

        self.state = State(self.system_config.get('influxdb', {}))
        self.scheduler = BackgroundScheduler(timezone=utc)

        self.load_nodes()
        self.load_conditions()

        pub.subscribe(self.stop, 'system.stop')
        pub.subscribe(self.restart, 'system.restart')

        LOGGER.debug('Initialized System')

    def start(self):
        """
        Starts the automation system
        """

        LOGGER.info('Starting')
        LOGGER.debug(f'System nodes: {self.nodes}')
        LOGGER.debug(f'System conditions: {self.conditions}')

        for node_label in self.nodes:
            LOGGER.debug(f'starting node {node_label}')
            pub.sendMessage(f'{node_label}.start')

        LOGGER.info('Starting scheduler')
        self.scheduler.start()

        LOGGER.info('Started')

    def stop(self):
        """
        Stops the automation system
        """

        LOGGER.info('Stopping')

        for node_label in self.nodes:
            LOGGER.debug(f'stopping node {node_label}')
            pub.sendMessage(f'{node_label}.stop')

        LOGGER.info('Stopping scheduler')
        self.scheduler.shutdown()

        LOGGER.info('Stopped')

    def restart(self):
        """
        Restarts the automation system
        """

        LOGGER.info('Restarting')
        self.stop()
        self.start()
        LOGGER.info('Restarted')

    def load_config(self):
        """
        Loads the 'config.yml' file
        """

        config_path = os.path.join(CONFIG_DIR, self.system_config_file)
        with open(config_path, 'r') as system_config_file:
            try:
                config = yaml.load(system_config_file)

                self.system_config = config.get('system', {})
                self.node_config = config.get('nodes', {})
                self.condition_config = config.get('conditions', {})

            except yaml.YAMLError as error:
                error_msg = f'Unable to read config.yml: {error}'
                raise Exception(error_msg)

    def load_nodes(self):
        """
        Loads nodes based on configuration in the config file
        """

        self.nodes = {}
        for label, node_contents in self.node_config.items():
            LOGGER.debug(f'Loading node {label}')
            node_name = node_contents['node']
            node_module = self.loaded_modules['nodes'][node_name]
            node_class = getattr(node_module, node_module.NODE_CLASS_NAME)
            node_config = node_contents.get('config')
            new_node = node_class(label, self.state, node_config)
            self.nodes[label] = new_node

    def load_conditions(self):
        """
        Loads conditions based on configuration in the config file
        """

        self.conditions = {}
        for condition_name, config in self.condition_config.items():

            schedule = None
            if config is not None:
                schedule = config.get('schedule')

            LOGGER.debug(f'Loading condition {condition_name}')
            condition_module = self.loaded_modules['conditions'][condition_name]
            condition_class = getattr(condition_module,
                                      condition_module.CONDITION_CLASS_NAME)
            new_condition = condition_class(self.scheduler, schedule)
            self.conditions[condition_name] = new_condition

    def load_packages(self):
        """
        Loads all packages from the package directory
        """

        packages_path = os.path.join(LOCAL_DIR, 'packages')
        with os.scandir(path=packages_path) as packages:
            for package in filter(lambda pkg: pkg.is_dir() and not
                                  pkg.name.startswith('__'), packages):
                package_path = os.path.join(packages_path, package.name)
                self.load_modules(package_path, package.name)

    def load_modules(self, package_path, package=None):
        """
        Loads a module from a package
        """

        if package is not None:
            package_name = f'.packages.{package}'
        else:
            package_name = ''

        for module_type in MODULE_TYPES:
            module_type_path = os.path.join(package_path, module_type)

            try:
                with os.scandir(path=module_type_path) as modules:
                    for module_file in modules:
                        if (module_file.name.endswith('.py') and not
                                module_file.name.startswith('__')):

                            module_file_name = f'{module_file.name[:-3]}'
                            module_name = f'{package_name}.{module_type}.{module_file_name}'
                            module = importlib.import_module(module_name, __package__)

                            if any(hasattr(module, class_name) for class_name in CLASS_NAME_CONSTS):
                                if package is not None:
                                    module_system_name = f'{package}.{module_file_name}'
                                else:
                                    module_system_name = module_file_name
                                LOGGER.info(f'Loaded module {module_system_name}')
                                self.loaded_modules[module_type][module_system_name] = module
            except FileNotFoundError:
                pass
