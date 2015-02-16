from actions import Action, CancelledActionException
import field
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


class TakeStoneAction(Action):
    """
    Accumulates x stone per turn
    """

    def __init__(self):
        self.current_stone = 0

    def update(self):
        self.current_stone += 1

    def process(self, player, **kwargs):
        player.stone += self.current_stone
        print "Took %s stone. Total stone: %s" % (self.current_stone, player.stone)
        self.current_stone = 0

    def describe(self):
        return 'Take %s stone.' % self.current_stone


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


class TakeSheepAction(Action):
    """
    Accumulates x sheep per turn
    """
    @classmethod
    def parse_coordinates(cls, coord_input):
        coords = list(coord_input.replace(" ", ""))
        x = int(coords[0])
        y = int(coords[1])
        return x, y

    def __init__(self):
        self.current_sheep = 0

    def update(self):
        self.current_sheep += 1

    def process(self, player, **kwargs):
        player.field.draw()
        correct_input = False
        while not correct_input:
            try:
                coordinates_input = raw_input('Where would you like to place the sheep? (eg \'31\' or \'3 1\')')
                if coordinates_input.lower() == 'cancel':
                    raise CancelledActionException()
                x, y = self.parse_coordinates(coordinates_input)
                player.field.update_node_animals(x, y, 'sheep', self.current_sheep)
                correct_input = True
            except ValueError as e:
                print e.message

        print 'Took %s sheep. Total cattle %s' % (self.current_sheep, player.cattle)
        self.current_sheep = 0

    def describe(self):
        return 'Take %s sheep.' % self.current_sheep


class TakeBoarAction(Action):
    """
    Accumulates x boar per turn
    """
    @classmethod
    def parse_coordinates(cls, coord_input):
        coords = list(coord_input.replace(" ", ""))
        x = int(coords[0])
        y = int(coords[1])
        return x, y

    def __init__(self):
        self.current_boar = 0

    def update(self):
        self.current_boar += 1

    def process(self, player, **kwargs):
        player.field.draw()
        correct_input = False
        while not correct_input:
            try:
                coordinates_input = raw_input('Where would you like to place the boar(s)? (eg \'31\' or \'3 1\')')
                if coordinates_input.lower() == 'cancel':
                    raise CancelledActionException()
                x, y = self.parse_coordinates(coordinates_input)
                player.field.update_node_animals(x, y, 'boar', self.current_boar)
                correct_input = True
            except ValueError as e:
                print e.message

        print 'Took %s boar(s). Total boar(s) %s.' % (self.current_boar, player.boar)
        self.current_boar = 0

    def describe(self):
        return 'Take %s boar.' % self.current_boar


class TakeCattleAction(Action):
    """
    Accumulates x cattle per turn
    """
    @classmethod
    def parse_coordinates(cls, coord_input):
        coords = list(coord_input.replace(" ", ""))
        x = int(coords[0])
        y = int(coords[1])
        return x, y
    
    def __init__(self):
        self.current_cattle = 0

    def update(self):
        self.current_cattle += 1

    def process(self, player, **kwargs):
        player.field.draw()
        correct_input = False
        while not correct_input:
            try:
                coordinates_input = raw_input('Where would you like to place the cattle? (eg \'31\' or \'3 1\')')
                if coordinates_input.lower() == 'cancel':
                    raise CancelledActionException()
                x, y = self.parse_coordinates(coordinates_input)
                player.field.update_node_animals(x, y, 'cattle', self.current_cattle)
                correct_input = True
            except ValueError as e:
                print e.message

        print 'Took %s cattle. Total cattle %s.' % (self.current_cattle, player.cattle)
        self.current_cattle = 0

    def describe(self):
        return 'Take %s cattle.' % self.current_cattle


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


class TakeVegetableAction(Action):
    """
    Does not accumulate.
    """

    def process(self, player, **kwargs):
        player.vegetable += 1
        print "Took 1 vegetable. Total vegetable: %s" % player.vegetable

    def describe(self):
        return 'Take 1 vegetable.'

    def update(self):
        pass


class TestAction(Action):
    """
    Filler while other actions are not yet implemented, does nothing
    """

    def update(self):
        pass

    def process(self, player, **kwargs):
        print "Took test action."

    def describe(self):
        return 'Filler action to be implemented later.'


class TestAction2(Action):
    """
    Filler while other actions are not yet implemented, does nothing
    """

    def update(self):
        pass

    def process(self, player, **kwargs):
        print "Took other test action!"

    def describe(self):
        return 'Filler action to be implemented later.'