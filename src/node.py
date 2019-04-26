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

    def update_state(self):
        """
        Updates the state, with the node's current state
        """

        raise NotImplementedError
