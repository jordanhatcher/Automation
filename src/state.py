"""
state

The state module contains the State class.
"""

import logging
from influxdb import InfluxDBClient
from pubsub import pub
from requests.exceptions import ConnectionError

LOGGER = logging.getLogger(__name__)

class State:
    """
    State

    The state class represents the state of the automation system. States are
    first keyed by the node label, then by the state key. Messages are
    published when a state's value is updated.
    """

    def __init__(self, settings):
        """
        Constructor
        """

        self.state_cache = {}
        self.db_disabled = False
        self.settings = settings
        #TODO support all InfluxDBClient settings
        self.client = InfluxDBClient(settings.get('host'),
                                     settings.get('port'),
                                     settings.get('user'),
                                     settings.get('pass'),
                                     settings.get('db_name'))
        LOGGER.info('Initialized State')

    def update_state(self, node_label, values):
        """
        Updates the state of a node. values should be a dict of key-value pairs
        to update the state of the node with. The latest values cached in a dict
        to avoid database calls when getting the most up-to-date values for a
        node's state. A message is published to the topic
        'state.<node_label>.<key>' for the values that are updated to activate
        conditions listening to the state.
        """

        LOGGER.debug(f'Updating state: {values}')

        points = []

        for key, value in values.items():
            self.state_cache.setdefault(node_label, {})
            self.state_cache[node_label].setdefault(key)

            previous_value = self.state_cache[node_label][key]
            self.state_cache[node_label][key] = value

            points.append({
                "measurement": key,
                "tags": {
                    "node_label": node_label
                },
                'fields': {
                    'value': value
                }
            })

            message = {
                'previous_value': previous_value,
                'value': value,
                'did_change': previous_value == value
            }

            pub.sendMessage(f'state.{node_label}.{key}', msg=message)

        if not self.db_disabled: # TODO re-enable db after a time period
            try:
                self.client.write_points(points)
            except ConnectionError:
                self.db_disabled = True
                LOGGER.warning('Unable to write state to influxdb. The database will be disabled, but state will be written to local cache.')
        else:
            LOGGER.warning('The database connection is disabled. Writting state to local cache.')
