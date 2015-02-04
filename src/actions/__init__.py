from actions.exceptions import CancelledActionException, InvalidActionException

__author__ = 'djw'
"""
This module houses all of the actions that a player may take over the course of a game
"""


class Action(object):
    """
    Actions are taken by players, they may have preconditions, postconditions, and may be mutated by each other
    """

    def process(self, player, **kwargs):
        """
        The main processing step of an action, mutations to external variables should be done here
        """
        raise NotImplementedError()

    def _pre_process_hook(self, player, **kwargs):
        """
        Run before the processing step of an action, useful for validating preconditions and/or determining parameters
        """
        pass

    def _post_process_hook(self, player, **kwargs):
        """
        Run after the processing step of an action, useful for notifying systems of mutations
        """
        pass

    def run(self, player=None, **kwargs):
        """
        Called by external systems to execute this action.
        :param: player, the player executing this action
        """
        self._pre_process_hook(player, **kwargs)
        self.process(player, **kwargs)
        self._post_process_hook(player, **kwargs)

    def update(self):
        """ Called at the very beginning of a new turn AFTER harvest """
        raise NotImplementedError()

    def describe(self):
        """
        Return a string representation of this action. An explanation of what it does.
        """
        raise NotImplementedError()


class CompositeAndOrAction(Action):
    """
    An action that consists of two possible subactions
    Either or both actions may be taken in any order
    """

    subactions = {}
    actions_to_run = []
    possible_actions = []

    def get_next_action_key(self):
        print 'You can perform either or both of the following actions:'
        for key in self.possible_actions:
            print '%s|%s' % (self.subactions[key].describe(), key.capitalize())
        action_input = raw_input('Which action should be done next? (Type "none" to skip an action)').lower()

        if action_input == 'none':
            return None
        elif action_input == 'cancel':
            raise CancelledActionException()
        elif action_input not in self.possible_actions:
            raise InvalidActionException('%s is not a valid action' % action_input)

        return action_input

    def determine_actions_to_run(self):
        while len(self.actions_to_run) < 2:
            try:
                key = self.get_next_action_key()
            except InvalidActionException as e:
                print e.message  # show them the error and ask again
                continue
            if not key:
                return  # return immediately if the user does not want to perform another subaction
            self.actions_to_run.append(self.subactions[key])
            self.possible_actions.remove(key)

    def run(self, player=None, **kwargs):
        # clear actions to run
        self.actions_to_run = []
        self.possible_actions = self.subactions.keys()

        self.determine_actions_to_run()

        for action in self.actions_to_run:
            action.run()