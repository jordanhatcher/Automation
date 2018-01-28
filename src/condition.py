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

    def __init__(self, module):
        """
        Constructor
        """

        self.module = module
