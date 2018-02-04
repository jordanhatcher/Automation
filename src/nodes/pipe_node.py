"""
pipe_node

This module contains the PipeNode class
"""

import os
import threading
from pubsub import pub
from ..node import Node

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

        pub.subscribe(self.stop, 'system.node.{}.stop'.format(self.label))
        pub.subscribe(self.start, 'system.node.{}.start'.format(self.label))

    def update_state(self):
        """
        Gets the state of the node.
        """

        state = {'running': not self.running_event.is_set()}
        self.state.update_states(self.label, **state)

    def stop(self):
        """
        Stops the node
        """

        self.running_event.set()
        with open(self.config['pipe_path'], 'w') as pipe:
            pipe.write(' ') # write whitespace to the pipe to unblock the open call in run()

        self.update_state()

    def run(self):
        """
        Run loop
        """

        pipe_path = self.config['pipe_path']
        if not os.path.exists(pipe_path):
            os.mkfifo(pipe_path)

        self.running_event.clear()
        self.update_state()

        while not self.running_event.is_set():
            with open(pipe_path, 'r') as pipe:
                while True:
                    line = pipe.read()
                    if not line:
                        break

                    pub.sendMessage('messages.{}'.format(self.label), msg={
                        'content': line
                    })
