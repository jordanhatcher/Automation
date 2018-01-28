"""
node

Contains the Node class.
"""

class Node():
    """
    Node

    Superclass for all nodes in the system. Acts as an interface for nodes.
    """

    def __init__(self, label, config=None):
        """
        Constructor
        """

        self.label = label
        self.config = config

    def state(self):
        """
        Gets the state of the node.
        """

        raise NotImplementedError
