import logging
from player.family_member import FamilyMember

__author__ = 'djw'
"""
This module houses the player class and game entities under its control
"""

class Player(object):
    """
    The representation of the player and his items/properties
    """

    def __init__(self):
        self.family_members = [FamilyMember(is_adult=True), FamilyMember(is_adult=True)]
        self.clay = 0
        self.reed = 0
        self.wood = 0
        self.grain = 0

    @property
    def has_idle_family_members(self):
        """ :return: True if the player has at least one idle family member """
        return next((fm for fm in self.family_members if fm.currently_working), None)

    def update(self):
        """ Called at the very beginning of a new turn AFTER harvest """
        logging.debug('Family Members before update: ')
        for member in self.family_members:
            logging.debug('Food cost: %s' % member.food_cost)
            logging.debug('Currently working: %s' % member.currently_working)
            member.update()

    def draw(self):
        print "Family Members: %s | Wood: %s | Clay: %s | Reed: %s" % \
              (len(self.family_members), self.wood, self.clay, self.reed)