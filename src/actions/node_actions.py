from actions import CompositeAndOrAction, Action, CancelledActionException
from actions.take import TestAction, TestAction2
from field import RoomItem
from field.node_item import StableItem

__author__ = 'djw'


class TestCompositeFieldAction(CompositeAndOrAction):
    """
    Filler while other actions are not yet implemented, does nothing
    """

    subactions = {
        'a': TestAction(),
        'b': TestAction2(),
    }

    def describe(self):
        return 'Composite and/or action to be implemented later.'


class BuildRoomAction(Action):
    """
    Builds a room in an available space on the player's field
    """

    @classmethod
    def parse_coordinates(cls, coord_input):
        coords = list(coord_input.replace(" ", ""))
        x = int(coords[0])
        y = int(coords[1])
        return x, y

    def update(self):
        pass

    def has_resources_for_room(self, material, player):
        if material == 'wood':
            return player.wood >= 5 and player.reed >= 2
        elif material == 'clay':
            return player.clay >= 5 and player.reed >= 2
        elif material == 'stone':
            return player.stone >= 5 and player.reed >= 2

    def process(self, player, **kwargs):
        material = player.field.room_material
        if not self.has_resources_for_room(material, player):
            raise CancelledActionException('Need 5 wood and 2 reed to build a room. ' +
                                           'You currently have %s wood and %s reed.' % (player.wood, player.reed))
        player.field.draw()

        correct_input = False
        while not correct_input:
            try:
                coordinates_input = raw_input('Write the coordinates of the new room: (eg \'31\' or \'3 1\')')
                if coordinates_input.lower() == 'cancel':
                    raise CancelledActionException()
                x, y = self.parse_coordinates(coordinates_input)
                player.field.add_item_to_node(x, y, RoomItem())
                correct_input = True
            except ValueError as e:
                print e.message

        self.adjust_player_resources(material, player)
        print 'Built a %s room' % material
        player.field.draw()

    def describe(self):
        return 'Build a new room for your house.'

    def adjust_player_resources(self, material, player):
        if material == 'wood':
            player.wood -= 5
        elif material == 'clay':
            player.clay -= 5
        elif material == 'stone':
            player.stone -= 5
        player.reed -= 2


class BuildStablesAction(Action):
    """
    Builds a number of stables in open spaces on the player's field
    """

    def describe(self):
        return 'Build stables for your field.'

    @classmethod
    def parse_coordinates(cls, coord_input):
        coords = list(coord_input.replace(" ", ""))
        x = int(coords[0])
        y = int(coords[1])
        return x, y

    def has_resources_for_stables(self, count, player):
        return player.wood >=2*int(count)

    def adjust_player_resources(self, count, player):
        player.wood = player.wood - 2*int(count)

    def process(self, player, **kwargs):
        player.field.draw()
        count = raw_input('How many stables to build?')
        if count == 'cancel':
            raise CancelledActionException()

        if not self.has_resources_for_stables(count, player):
            raise CancelledActionException('Need %s wood for %s stables; you have %s wood.' %
                                           (2*int(count), count, player.wood))
        stablesBuilt = 0
        while stablesBuilt != int(count):
            try:
                coordinates_input = raw_input('Write the coordinates of stables %s: (eg \'31\' or \'3 1\')')
                if coordinates_input.lower() == 'cancel':
                    raise CancelledActionException()
                x, y = self.parse_coordinates(coordinates_input)
                player.field.add_item_to_node(x, y, StableItem())
                stablesBuilt += 1
            except ValueError as e:
                print e.message

        self.adjust_player_resources(count, player)
        print 'Built %s stables.' % count
        player.field.draw()

    def update(self):
        pass