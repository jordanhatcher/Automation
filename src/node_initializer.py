"""
Helper to initialize nodes from loaded modules
"""

import logging

LOGGER = logging.getLogger(__name__)

def init_nodes(node_config, state, loaded_modules):
    """
    Initializes nodes based on configuration in the config file
    """

    nodes = {}

    for label, node_contents in node_config.items():
        LOGGER.debug(f'Loading node {label}')
        node_type = node_contents['node_type']
        node_module = loaded_modules[node_type]
        node_class = getattr(node_module, node_module.NODE_CLASS_NAME)
        node_specific_config = node_contents.get('config')
        new_node = node_class(label, state, node_specific_config)
        nodes[label] = new_node

    return nodes
