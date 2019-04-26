"""
condition

Contains the Condition class
"""

from pubsub import pub


class Condition():
    """
    Condition

    Represents a condition that performs actions when certain conditions are
    met. This class is a superclass that all other conditions extend.
    """

    def __init__(self, scheduler, schedule=None, inputs=None, outputs=None):
        """
        Constructor
        """

        self.scheduler = scheduler
        self.schedule = schedule
        self.inputs = inputs or []
        self.outputs = outputs or []

        self._subscribe_to_inputs()

    def _subscribe_to_inputs(self):
        """
        Subscribe the evaluate method to all input topics
        """

        for inpt in self.inputs:
            pub.subscribe(self.evaluate, inpt)

    def evaluate(self, msg=None):
        """
        Each condition should provide its own implementation of the evaluate
        method, which gets subscribed to input messages and schedules, and
        publishes the result of the evaluation to the outputs.
        """
        raise NotImplementedError

    def is_active(self):
        """
        Conditions will override this method to implement custom logic for
        checking if the condition is active or not. The default is that the
        condition will be active.
        """

        return True


def link(func):
    """
    Decorates a function to automatically publish the function's return value
    to all of the function's outputs.
    """

    def wrapper(self, msg):
        output_msg = func(self, msg)
        if output_msg is not None:
            for output in self.outputs:
                if not output.startswith('system'):
                    pub.sendMessage(output, msg=output_msg)
                else:
                    pub.sendMessage(output)
    return wrapper
