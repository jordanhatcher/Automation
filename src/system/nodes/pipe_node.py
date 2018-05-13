"""
pipe_node

This module contains the PipeNode class
"""

import logging
import os
import threading
from pubsub import pub
from ..node import Node

LOGGER = logging.getLogger(__name__)

NODE_CLASS_NAME = 'PipeNode'

class PipeNode(Node, threading.Thread):
    """
    PipeNode

    Creates a named pipe that can be used to send basic commands to the
    automation system.
    """

    def __init__(self, label, state, config=None):
        """
        Constructor
        """

        Node.__init__(self, label, state, config)
        threading.Thread.__init__(self)

        self.running_event = threading.Event()
        self.state.add_states(self.label, ['running'])

        pub.subscribe(self.stop, f'{self.label}.stop')
        pub.subscribe(self.start, f'{self.label}.start')

        LOGGER.debug(f'Initialized {self.label}')

    def update_state(self):
        """
        Gets the state of the node.
        """

        LOGGER.info(f'Updating state {self.label}')
        state = {'running': not self.running_event.is_set()}
        self.state.update_states(self.label, **state)

    def stop(self):
        """
        Stops the node
        """

        LOGGER.info(f'Stopping {self.label}')
        self.running_event.set()
        with open(self.config['pipe_path'], 'w') as pipe:
            pipe.write(' ') # write whitespace to the pipe to unblock the open call in run()

        self.update_state()
        LOGGER.info(f'Stopped {self.label}')

    def run(self):
        """
        Run loop
        """

        LOGGER.info(f'Started {self.label}')

        pipe_path = self.config['pipe_path']
        if not os.path.exists(pipe_path):
            os.makedirs(os.path.dirname(pipe_path), exist_ok=True)
            os.mkfifo(pipe_path)

        self.running_event.clear()
        self.update_state()

        while not self.running_event.is_set():
            with open(pipe_path, 'r') as pipe:
                while True:
                    line = pipe.read()
                    if not line:
                        break

                    LOGGER.info('Received input')
                    LOGGER.debug('Input: %s', line)
                    pub.sendMessage(f'messages.{self.label}', msg={
                        'content': line
                    })
