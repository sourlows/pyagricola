import copy
import logging
from random import shuffle
__author__ = 'djw'


class GameBoard(object):
    """
    Manages the game board and actions available to the player
    """
    DEFAULT_ACTIONS = {
        'Rooms': 'Build rooms and/or Build stables action here',
        'Starting': 'Starting player and/or build minor improvement action here',
        'Grain': 'Take grain action here',
        'Plow': 'Plow field action here',
        'Occupation': 'Occupation action here',
        'Laborer': 'Day laborer action here',
        'Wood': 'Take wood action here',
        'Clay': 'Take clay action here',
        'Reed': 'Take reed action here',
        'Fishing': 'Take fishing action here',
    }

    STAGE_ONE_ACTIONS = {
        'Sheep': 'Take sheep action here',
        'Sow': 'Sow and/or Bake bread action here',
        'Improvement': 'Build major/minor Improvement action here',
        'Fences': 'Improvement action here',
    }

    STAGE_TWO_ACTIONS = {
        'Renovate': 'Renovate + build improvement action here',
        'Stone': 'Take stone action here',
        'Growth': 'Family growth + build minor improvement action here',
    }

    STAGE_THREE_ACTIONS = {
        'Boar': 'Take boar action here',
        'Vegetable': 'Take vegetable action here',
    }

    STAGE_FOUR_ACTIONS = {
        'Cattle': 'Take cattle action here',
        'Stone2': 'Take stone action here',
    }

    STAGE_FIVE_ACTIONS = {
        'PlowAndSow': 'Plow field and sow action here',
        'Overgrowth': 'Family growth without room action here',
    }

    STAGE_SIX_ACTIONS = {
        'RenovateFence': 'Renovate and build fences action here',
    }

    def __init__(self):
        self.available_actions = copy.deepcopy(self.DEFAULT_ACTIONS)

        # determine the order in which actions will become available to the player (random)
        self._upcoming_actions_keys = []
        self._upcoming_actions_keys.extend(self._get_shuffled_keys_for_dict(self.STAGE_ONE_ACTIONS))
        self._upcoming_actions_keys.extend(self._get_shuffled_keys_for_dict(self.STAGE_TWO_ACTIONS))
        self._upcoming_actions_keys.extend(self._get_shuffled_keys_for_dict(self.STAGE_THREE_ACTIONS))
        self._upcoming_actions_keys.extend(self._get_shuffled_keys_for_dict(self.STAGE_FOUR_ACTIONS))
        self._upcoming_actions_keys.extend(self._get_shuffled_keys_for_dict(self.STAGE_FIVE_ACTIONS))
        self._upcoming_actions_keys.extend(self._get_shuffled_keys_for_dict(self.STAGE_SIX_ACTIONS))

        # build a directory of all actions for lookup purposes only
        self._all_actions = copy.deepcopy(self.DEFAULT_ACTIONS)
        self._all_actions.update(self.STAGE_ONE_ACTIONS)
        self._all_actions.update(self.STAGE_TWO_ACTIONS)
        self._all_actions.update(self.STAGE_THREE_ACTIONS)
        self._all_actions.update(self.STAGE_FOUR_ACTIONS)
        self._all_actions.update(self.STAGE_FIVE_ACTIONS)
        self._all_actions.update(self.STAGE_SIX_ACTIONS)

    def _get_shuffled_keys_for_dict(self, any_dict):
        """
        :return: the keys of any_dict in random order
        """
        keys = any_dict.keys()
        shuffle(keys)
        return keys

    def update(self):
        """ Called at the very beginning of a new turn AFTER harvest """
        if not self._upcoming_actions_keys:
            logging.error('No more upcoming actions')
            return

        # make the next action available
        next_action_key = self._upcoming_actions_keys.pop(0)
        self.available_actions.update({next_action_key: self._all_actions[next_action_key]})
        logging.debug('Available actions: %s', self.available_actions)