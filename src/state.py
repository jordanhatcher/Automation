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

    def add_states(self, node_label, keys):
        """
        Helper function to add new state keys for a node label.
        """

        for key in keys:
            self.state_dict[node_label][key] = None

    def update_states(self, node_label, **states):
        """
        Updates states (keys) of a node (node_label) with new values. A
        message is published to the topic 'state.<node_label>.<key>' for the
        values that are updated to activate conditions listening to the state.
        """

        for key in states:
            value = states[key]
            previous_value = self.state_dict[node_label][key]

            if not value == previous_value:
                self.state_dict[node_label][key] = value
                topic = 'state.{}.{}'.format(node_label, key)
                message = {'previous_value': previous_value, 'value': value}
                pub.sendMessage(topic, **message)
