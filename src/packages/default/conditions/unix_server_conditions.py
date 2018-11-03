"""
unix_server_conditions

"""

import logging
from pubsub import pub
from condition import Condition

LOGGER = logging.getLogger(__name__)

CONDITION_CLASS_NAME = 'UnixServerConditions'

class UnixServerConditions(Condition):
    """
    UnixServerConditions

    Conditions for handling messages sent to the UnixSocketServer
    node
    """

    def __init__(self, scheduler, schedule=None):
        """
        Constructor
        """

        Condition.__init__(self, scheduler, schedule)
        pub.subscribe(self.evaluate, 'messages.unix_socket_node')
        LOGGER.debug('Initialized')

    def evaluate(self, msg):
        """
        Handler for receiving messages
        """

        LOGGER.info('Evaluating')
        print(msg)

        if 'stop' in msg['content']:
            pub.sendMessage('system.stop')
