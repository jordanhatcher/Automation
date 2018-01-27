"""
state

The state module contains the State class.
"""

from pubsub import pub

class State:
    """
    State

    The state class represents the state of the automation system. States are
    first keyed by the node label, then by the state key. Messages are
    published when a state's value is updated.
    """

    def __init__(self):
        """
        Constructor
        """

        self.state_dict = {}

    def add_node(self, node_label):
        """
        Adds a new node label to the state dictionary.
        """

        self.state_dict[node_label] = {}

    def add_state(self, node_label, key):
        """
        Helper function to add a new state key for a node label.
        """

        self.state_dict[node_label][key] = None

    def update_state(self, node_label, key, value):
        """
        Updates a state (key) of a node (node_label) with a new value. A
        message is published to the topic 'state.<node_label>.<key>' once
        the value is updated to activate conditions listening to the state.
        """

        previous_value = self.state_dict[node_label][key]
        self.state_dict[node_label][key] = value
        topic = 'state.{}.{}'.format(node_label, key)
        message = {'previous_value': previous_value, 'value': value}
        pub.sendMessage(topic, **message)
