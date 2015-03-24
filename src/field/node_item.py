__author__ = 'djw'


class FieldNodeItem(object):
    """
    An item built on a player's field board, held within a node/cell on that board
    """

    def __init__(self):
        self.cattle = 0
        self.boars = 0
        self.sheep = 0
        self.grain = 0
        self.vegetables = 0

    def update_animals(self, animal, count):
        if animal == 'sheep':
            self.sheep += count
        if animal == 'boar':
            self.boars += count
        if animal == 'cattle':
            self.cattle += count

    def update_crop(self, crop):
        if crop == 'grain':
            self.grain += 3
        if crop == 'vegetables':
            self.vegetables += 2

    @property
    def has_resources(self):
        num_resources = self.cattle + self.boars + self.sheep + self.grain + self.vegetables
        return num_resources > 0

    def update(self):
        """ Called every turn """
        raise NotImplementedError()

    def harvest(self, player):
        """ Initiates and controls the harvest process for this item """
        return

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
        super(RoomItem, self).__init__()
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


class PlowedFieldItem(FieldNodeItem):
    """
    A space on the player's field board that has been plowed and can be sowed upon
    """

    def update(self):
        pass

    def score(self):
        return 1

    def harvest(self, player):
        # harvest crops
        if self.grain > 0:
            self.grain -= 1
            player.grain += 1
        elif self.vegetables > 0:
            self.vegetables -= 1
            player.vegetable += 1


    def describe(self):
        return u"\u25A7" # Square with upper left to lower right fill