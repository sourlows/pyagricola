import logging
from field import Field
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
        self.stone = 0
        self.grain = 0
        self.vegetable = 0
        self.sheep = 0
        self.boar = 0
        self.cattle = 0
        self.food = 2
        self.field = Field()

    @property
    def has_idle_family_members(self):
        """ :return: True if the player has at least one idle family member """
        return next((fm for fm in self.family_members if not fm.currently_working), None)

    def send_family_member_to_work(self):
        """"
        Get the next idle family member and mark them as currently working
        :raise: ValueError if there are no idle family members
        """
        next_fm = next((fm for fm in self.family_members if not fm.currently_working), None)
        if not next_fm:
            raise ValueError('No idle family members.')

        next_fm.currently_working = True

    def update(self):
        """ Called at the very beginning of a new turn AFTER harvest """
        logging.debug('Family Members before update: ')
        for member in self.family_members:
            logging.debug('Food cost: %s' % member.food_cost)
            logging.debug('Currently working: %s' % member.currently_working)
            member.update()

    def draw(self):
        print "Family Members: %s | Food: %s | Wood: %s | Clay: %s | Reed: %s | Grain: %s | Vegetable: %s | Sheep: %s | Boar: %s | Cattle: %s" % \
              (len(self.family_members), self.food, self.wood, self.clay, self.reed,
               self.grain, self.vegetable, self.sheep, self.boar, self.cattle)