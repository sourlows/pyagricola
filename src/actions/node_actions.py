from actions import CompositeAndOrAction, Action, CancelledActionException, parse_coordinates, is_whole_number
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
                x, y = parse_coordinates(coordinates_input)
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

    def has_resources_for_stables(self, num_stables, player):
        return player.wood >= 2*num_stables

    def adjust_player_resources(self, num_stables, player):
        player.wood -= 2*num_stables

    def process(self, player, **kwargs):
        player.field.draw()

        correct_input = False
        while not correct_input:
            num_stables = raw_input('How many stables to build?')
            if num_stables == 'cancel':
                raise CancelledActionException()
            if is_whole_number(num_stables):
                num_stables = int(num_stables)
                correct_input = True
            else:
                print '%s is not a whole number, please try again.' % num_stables

        if not self.has_resources_for_stables(num_stables, player):
            raise CancelledActionException('Need %s wood for %s stables; you have %s wood.' %
                                           (2*num_stables, num_stables, player.wood))
        stables_built = 0
        while stables_built != num_stables:
            try:
                coordinates_input = raw_input('Write the coordinates of stables %s: (eg \'31\' or \'3 1\')')
                if coordinates_input.lower() == 'cancel':
                    raise CancelledActionException()
                x, y = parse_coordinates(coordinates_input)
                player.field.add_item_to_node(x, y, StableItem())
                stables_built += 1
            except ValueError as e:
                print e.message

        self.adjust_player_resources(num_stables, player)
        print 'Built %s stables.' % num_stables
        player.field.draw()

    def update(self):
        pass


class RoomsOrStablesAction(CompositeAndOrAction):
    """
    Filler while other actions are not yet implemented, does nothing
    """

    subactions = {
        'rooms': BuildRoomAction(),
        'stables': BuildStablesAction(),
    }

    def describe(self):
        return 'Build a room and/or stables'