"""
pipe_conditions

"""

from pubsub import pub
from ..condition import Condition

CONDITION_CLASS_NAME = 'PipeConditions'

class PipeConditions(Condition):
    """
    PipeConditions

    Conditions for reading from named pipes
    """

    def __init__(self):
        """
        Constructor
        """
        Condition.__init__(self, 'pipe_conditions')
        pub.subscribe(self.evaluate, 'messages.pipe_node')

    def evaluate(self, msg):
        """
        Handler for receiving messages
        """

        if 'stop' in msg['content']:
            pub.sendMessage('system.stop')
