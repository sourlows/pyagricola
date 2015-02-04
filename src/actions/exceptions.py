__author__ = 'djw'


class CancelledActionException(Exception):
    """
    Raised when an action is cancelled
    """
    pass


class InvalidActionException(Exception):
    """
    Raised when an action is impossible to execute
    """
    pass