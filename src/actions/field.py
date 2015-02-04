from actions import CompositeAndOrAction
from actions.take import TestAction, TestAction2

__author__ = 'djw'


class TestCompositeFieldAction(CompositeAndOrAction):
    """
    Filler while other actions are not yet implemented, does nothing
    """

    subactions = {
        'a': TestAction(),
        'b': TestAction2(),
    }

    def describe(self):
        return 'Composite and/or action to be implemented later.'