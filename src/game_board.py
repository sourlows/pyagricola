import copy
import logging
from random import shuffle
from actions import CancelledActionException
from actions.node_actions import TestCompositeFieldAction, BuildRoomAction, BuildStablesAction
from actions.take import TakeWoodAction, TakeReedAction, TakeClayAction, TestAction, TakeGrainAction, TakeFishingAction, TakeDayLaborerAction, TakeSheepAction, TakeStoneAction, TakeBoarAction, TakeCattleAction, TakeVegetableAction

__author__ = 'djw'


class ActionSpace(object):
    """
    A space on the gameboard that allows a player to perform an action
    """

    def __init__(self, action):
        self.action = action
        self.is_occupied = False

    def take(self, player):
        """
        Occupy this space and execute its action(s)
        """
        self.is_occupied = True
        try:
            self.action.run(player=player)
        except CancelledActionException as e:
            self.is_occupied = False
            raise e

    def update(self):
        self.is_occupied = False
        self.action.update()

    def describe(self):
        occupied_char = "x" if self.is_occupied else "_"
        return "|%s|%s" % (occupied_char, self.action.describe())


class GameBoard(object):
    """
    Manages the game board and actions available to the player
    """
    DEFAULT_ACTIONS = {
        'rooms': ActionSpace(action=BuildRoomAction()),
        'stables': ActionSpace(action=BuildStablesAction()),
        'starting': ActionSpace(action=TestAction()),
        'grain': ActionSpace(action=TakeGrainAction()),
        'plow': ActionSpace(action=TestAction()),
        'occupation': ActionSpace(action=TestAction()),
        'laborer': ActionSpace(action=TakeDayLaborerAction()),
        'wood': ActionSpace(action=TakeWoodAction()),
        'clay': ActionSpace(action=TakeClayAction()),
        'reed': ActionSpace(action=TakeReedAction()),
        'fishing': ActionSpace(action=TakeFishingAction()),
    }

    STAGE_ONE_ACTIONS = {
        'sheep': ActionSpace(action=TakeSheepAction()),
        'sow': ActionSpace(action=TestAction()),
        'improvement': ActionSpace(action=TestAction()),
        'fences': ActionSpace(action=TestAction()),
    }

    STAGE_TWO_ACTIONS = {
        'renovate': ActionSpace(action=TestAction()),
        'stone': ActionSpace(action=TakeStoneAction()),
        'growth': ActionSpace(action=TestAction()),
    }

    STAGE_THREE_ACTIONS = {
        'boar': ActionSpace(action=TakeBoarAction()),
        'vegetable': ActionSpace(action=TakeVegetableAction()),
    }

    STAGE_FOUR_ACTIONS = {
        'cattle': ActionSpace(action=TakeCattleAction()),
        'stone2': ActionSpace(action=TakeStoneAction()),
    }

    STAGE_FIVE_ACTIONS = {
        'plowandsow': ActionSpace(action=TestAction()),
        'overgrowth': ActionSpace(action=TestAction()),
    }

    STAGE_SIX_ACTIONS = {
        'renovatefence': ActionSpace(action=TestAction()),
    }

    def __init__(self):
        self.available_actions = copy.deepcopy(self.DEFAULT_ACTIONS)

        all_stages = [self.STAGE_ONE_ACTIONS, self.STAGE_TWO_ACTIONS, self.STAGE_THREE_ACTIONS, self.STAGE_FOUR_ACTIONS,
                      self.STAGE_FIVE_ACTIONS, self.STAGE_SIX_ACTIONS]

        # a list of the keys of upcoming actions, with the first element being the key for the next available action
        self._upcoming_actions_keys = []

        # a directory of all possible board actions for lookup purposes only
        self._all_actions = copy.deepcopy(self.DEFAULT_ACTIONS)

        for stage in all_stages:
            # determine the order in which actions will become available to the player (random)
            self._upcoming_actions_keys.extend(self._get_shuffled_keys_for_dict(stage))
            self._all_actions.update(stage)

    def _get_shuffled_keys_for_dict(self, any_dict):
        """
        :return: the keys of any_dict in random order
        """
        keys = any_dict.keys()
        shuffle(keys)
        return keys

    def update(self):
        """ Called at the very beginning of a new turn """
        if not self._upcoming_actions_keys:
            logging.error('No more upcoming actions')
            return

        # make the next action available
        next_action_key = self._upcoming_actions_keys.pop(0)
        self.available_actions.update({next_action_key: self._all_actions[next_action_key]})

        for key, action_space in self.available_actions.iteritems():
            action_space.update()

    def draw(self):
        for key, action_space in self.available_actions.iteritems():
            print '%s|%s' % (action_space.describe(), key.capitalize())