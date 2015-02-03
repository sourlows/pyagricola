from actions import Action
__author__ = 'djw'


class TakeClayAction(Action):
    """
    Accumulates x clay per turn
    """

    def __init__(self):
        self.current_clay = 0

    def update(self):
        self.current_clay += 1

    def process(self, player, **kwargs):
        player.clay += self.current_clay
        print "Took %s clay. Total clay: %s" % (self.current_clay, player.clay)
        self.current_clay = 0

    def describe(self):
        return 'Take %s clay.' % self.current_clay


class TakeReedAction(Action):
    """
    Accumulates x reed per turn
    """

    def __init__(self):
        self.current_reed = 0

    def update(self):
        self.current_reed += 1

    def process(self, player, **kwargs):
        player.reed += self.current_reed
        print "Took %s reed. Total reed: %s" % (self.current_reed, player.reed)
        self.current_reed = 0

    def describe(self):
        return 'Take %s reed.' % self.current_reed


class TakeWoodAction(Action):
    """
    Accumulates x wood per turn
    """

    def __init__(self):
        self.current_wood = 0

    def update(self):
        self.current_wood += 3

    def process(self, player, **kwargs):
        player.wood += self.current_wood
        print "Took %s wood. Total wood: %s" % (self.current_wood, player.wood)
        self.current_wood = 0

    def describe(self):
        return 'Take %s wood.' % self.current_wood


class TakeFishingAction(Action):
    """
    Accumulates x food per turn
    """

    def __init__(self):
        self.current_food = 0

    def update(self):
        self.current_food += 1

    def process(self, player, **kwargs):
        player.food += self.current_food
        print "Took %s food. Total food: %s" % (self.current_food, player.food)
        self.current_food = 0

    def describe(self):
        return 'Take %s food.' % self.current_food


class TakeDayLaborerAction(Action):
    """
    Does not accumulate.
    """

    def process(self, player, **kwargs):
        player.food += 2
        print "Took 2 food. Total food: %s" % player.food

    def describe(self):
        return 'Take 2 food.'

    def update(self):
        pass


class TakeGrainAction(Action):
    """
    Does not accumulate.
    """

    def process(self, player, **kwargs):
        player.grain += 1
        print "Took 1 grain. Total grain: %s" % player.grain

    def describe(self):
        return 'Take 1 grain.'

    def update(self):
        pass


class TestAction(Action):
    """
    Filler while other actions are not yet implemented, does nothing
    """

    def update(self):
        pass

    def process(self, player, **kwargs):
        pass

    def describe(self):
        return 'Filler action to be implemented later.'