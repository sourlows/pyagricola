__author__ = 'djw'


class FieldNodeItem(object):
    """
    An item built on a player's field board, held within a node/cell on that board
    """

    def update(self):
        """ Called every turn """
        raise NotImplementedError()

    def harvest(self):
        """ Initiates and controls the harvest process for this item """
        pass

    def score(self):
        """
        Calculates and returns the current score of this item.
        """
        raise NotImplementedError()

    def describe(self):
        """
        Return the current state of this item as a string that will be drawn
        """
        raise NotImplementedError()


class RoomItem(FieldNodeItem):
    """
    A single room on a player's field board
    """
    MATERIAL_CHOICES = frozenset(['wood', 'stone', 'clay'])

    def __init__(self, material='wood'):
        if material not in self.MATERIAL_CHOICES:
            raise ValueError('Invalid material %s not in %s' % (material, self.MATERIAL_CHOICES))
        self.material = material

    def set_material(self, material):
        if material not in self.MATERIAL_CHOICES:
            raise ValueError('Invalid material %s not in %s' % (material, self.MATERIAL_CHOICES))
        self.material = material

    def update(self):
        pass  # rooms do not update from turn to turn

    def score(self):
        if self.material == 'wood':
            return 0
        elif self.material == 'clay':
            return 1
        elif self.material == 'stone':
            return 2

    def describe(self):
        return u"\u25A1"  # white square (unicode)

class StableItem(FieldNodeItem):
    """
    A stable on the player's field board
    """

    def update(self):
        pass

    def score(self):
        return 1

    def describe(self):
        return u"\u039E" # Greek letter Xi (unicode)