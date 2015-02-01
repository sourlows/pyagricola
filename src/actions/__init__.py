__author__ = 'djw'
"""
This module houses all of the actions that a player may take over the course of a game
"""


class Action(object):
    """
    Actions are taken by players, they may have preconditions, postconditions, and may be mutated by each other
    """

    def process(self, **kwargs):
        """
        The main processing step of an action, mutations to external variables should be done here
        """
        raise NotImplementedError()

    def _pre_process_hook(self, **kwargs):
        """
        Run before the processing step of an action, useful for validating preconditions and/or determining parameters
        """
        pass

    def _post_process_hook(self, **kwargs):
        """
        Run after the processing step of an action, useful for notifying systems of mutations
        """
        pass

    def run(self, **kwargs):
        self._pre_process_hook(**kwargs)
        self.process(**kwargs)
        self._post_process_hook(**kwargs)