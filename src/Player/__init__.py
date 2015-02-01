import logging
from Player.family_member import FamilyMember

__author__ = 'djw'
"""
This module houses the Player class and game entities under its control
"""

class Player(object):
    """
    The representation of the Player and his items/properties
    """

    def __init__(self):
        self.family_members = [FamilyMember(is_adult=True), FamilyMember()]

    def update(self):
        """ Called at the very beginning of a new turn AFTER harvest """
        logging.debug('Family Members before update: ')
        for member in self.family_members:
            logging.debug('Food cost: %s' % member.food_cost)
            logging.debug('Currently working: %s' % member.currently_working)
            member.update()