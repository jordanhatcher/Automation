"""
main

Main entrypoint for the automation system
"""

import logging
from system.system import System

FORMAT = '[%(asctime)s] %(levelname)s - %(name)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

SYSTEM = System()
SYSTEM.start()
