"""
system

The system module contains the system class
"""

### IMPORTS ###
import logging
import os
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
from pubsub import pub

from state import State
from config_loader import load_config
from node_initializer import init_nodes
from condition_initializer import init_conditions
from package_module_loader import load_package_modules

LOG_FORMAT = '[%(asctime)s] %(levelname)s - %(name)s - %(message)s'

#### CONSTANTS ####
LOGGER = logging.getLogger(__name__)
LOCAL_DIR = os.path.dirname(__file__)
CONFIG_DIR = os.path.join(LOCAL_DIR, 'config')
###

# 1. get config
system_config, node_config, condition_config = load_config(CONFIG_DIR)

# Set up logging
log_level = logging.getLevelName(system_config.get('log_level', 'INFO').upper())
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)

# initialize state, event loops, scheduler, etc
state = State(system_config.get('influxdb', {}))
event_loop = asyncio.get_event_loop()
scheduler = AsyncIOScheduler(timezone=utc)

# Pre-load modules
loaded_modules = load_package_modules(LOCAL_DIR)

# Init configured modules
nodes = init_nodes(node_config, state, loaded_modules)
conditions = init_conditions(condition_config, scheduler, loaded_modules)

# Start the system
try:
    scheduler.start()

    for node in nodes:
        task = node.get_task()
        if task: # only add nodes that have tasks to the event loop
            event_loop.add_task(task)

    event_loop.run_forever()
except:
    LOGGER.info('Exiting')
