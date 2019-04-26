"""
unix_server_conditions

"""

import logging
from pubsub import pub
from condition import Condition, link

LOGGER = logging.getLogger(__name__)

CONDITION_CLASS_NAME = 'UnixServerConditions'

class UnixServerConditions(Condition):
    """
    UnixServerConditions

    Conditions for handling messages sent to the UnixSocketServer
    node
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor
        """

        super().__init__(*args, **kwargs)
        LOGGER.debug('Initialized')

    @link
    def evaluate(self, msg):
        """
        Handler for receiving messages
        """

        LOGGER.info('Evaluating')

        if 'stop' == msg['content'].strip():
            return True
