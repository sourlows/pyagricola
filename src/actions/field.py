from actions import CompositeAndOrAction, Action
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


class BuildRoomAction(Action):
    """
    Builds a room in an available space on the player's field
    """

    def __init__(self):
        self.material = None

    def update(self):
        pass

    def process(self, player, **kwargs):
        # TODO: set material
        # TODO: validate player has resources
        player.draw()
        # TODO: ask for build coordinates
        # TODO: try build, catch errors

    def describe(self):
        return 'Build a new room for your house.'