__author__ = 'djw'

class FamilyMember(object):
    """
    A single family member and his current state
    """

    def __init__(self, is_adult=False):
        self.is_adult = is_adult
        self.currently_working = False

    @property
    def food_cost(self):
        """ :return: The number of food this unit requires at harvest """
        return 2 if self.is_adult else 1

    def update(self):
        """ Called at the very beginning of a new turn AFTER harvest """
        if not self.is_adult:
            self.is_adult = True  # family members are only newborn on the turn they are created
        self.currently_working = False