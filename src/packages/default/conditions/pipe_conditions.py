"""
pipe_conditions

"""

import logging
from pubsub import pub
from condition import Condition

LOGGER = logging.getLogger(__name__)

CONDITION_CLASS_NAME = 'PipeConditions'

class PipeConditions(Condition):
    """
    PipeConditions

    Conditions for reading from named pipes
    """

    def __init__(self, scheduler, schedule=None):
        """
        Constructor
        """

        Condition.__init__(self, scheduler, schedule)
        pub.subscribe(self.evaluate, 'messages.pipe_node')
        LOGGER.debug('Initialized')

    def evaluate(self, msg):
        """
        Handler for receiving messages
        """

        LOGGER.info('Evaluating')

        if 'stop' in msg['content']:
            pub.sendMessage('system.stop')
