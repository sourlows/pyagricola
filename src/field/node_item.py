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
        self._material = material

    def set_material(self, material):
        if material not in self.MATERIAL_CHOICES:
            raise ValueError('Invalid material %s not in %s' % (material, self.MATERIAL_CHOICES))
        self._material = material

    def update(self):
        pass  # rooms do not update from turn to turn

    def score(self):
        if self._material == 'wood':
            return 0
        elif self._material == 'clay':
            return 1
        elif self._material == 'stone':
            return 2

    def describe(self):
        return u"\u25A1"  # white square (unicode)
