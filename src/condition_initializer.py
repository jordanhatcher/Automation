"""
Helper to initialize conditions from imported modules
"""

import logging
LOGGER = logging.getLogger(__name__)

def init_conditions(condition_config, scheduler, loaded_modules):
    """
    Loads conditions based on configuration in the config file
    """

    conditions = {}
    for condition_name, config in condition_config.items():

        schedule = None
        if config is not None:
            schedule = config.get('schedule')

        LOGGER.debug(f'Loading condition {condition_name}')
        condition_module = loaded_modules[condition_name]
        condition_class = getattr(condition_module,
                                  condition_module.CONDITION_CLASS_NAME)

        if schedule is not None:
            new_condition = condition_class(scheduler, schedule)
        else:
            new_condition = condition_class(scheduler)

        conditions[condition_name] = new_condition
    return conditions
