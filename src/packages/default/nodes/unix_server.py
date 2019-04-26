"""
unix_server

This module contains the UnixServerNode class
"""

import asyncio
import logging
import os
from pubsub import pub
from node import Node

LOGGER = logging.getLogger(__name__)

NODE_CLASS_NAME = 'UnixServerNode'

class UnixServerNode(Node):
    """
    UnixServerNode

    Creates a unix socket that can be used to send basic commands to the
    automation system.
    """

    def __init__(self, label, state, config=None):
        """
        Constructor
        """

        Node.__init__(self, label, state, config)

        socket_file = config['socket_path']

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.start_unix_server(self.handler, path=socket_file))

        LOGGER.info(f'Initialized {self.label}, starting unix server')

    def update_state(self):
        """
        Gets the state of the node.
        """

        LOGGER.info(f'Updating state {self.label}')
        self.state.update_state(self.label, state)

    async def handler(self, reader, writer):
        """
        Run loop
        """


        data = await reader.read(1000)

        LOGGER.info('Received unix socket input')

        message = data.decode()
        LOGGER.debug(f'Received: {message}')
        pub.sendMessage(f'messages.{self.label}', msg={
            'content': message
        })
