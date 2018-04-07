"""
condition

Contains the Condition class
"""

class Condition():
    """
    Condition

    Represents a condition that performs actions when certain conditions are
    met. This class is a superclass that all other conditions extend.
    """

    def __init__(self, scheduler, schedule=None):
        """
        Constructor
        """

        self.scheduler = scheduler
        self.schedule = schedule

    def is_active(self):
        """
        Conditions will override this method to implement custom logic for
        checking if the condition is active or not. The default is that the
        condition will be active.
        """

        return True
