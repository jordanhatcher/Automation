"""
node

Contains the Node class.
"""

class Node():
    """
    Node

    Superclass for all nodes in the system. Acts as an interface for nodes.
    """

    def __init__(self, label, state, config=None):
        """
        Constructor
        """

        self.label = label
        self.state = state
        self.config = config

        self._add_node_to_state()

    def _add_node_to_state(self):
        """
        Adds the node label to the system state.
        """

        self.state.add_node(self.label)

    def update_state(self):
        """
        Updates the state, with the node's current state
        """

        raise NotImplementedError
