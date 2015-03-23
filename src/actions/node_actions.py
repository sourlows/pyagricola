from actions import CompositeAndOrAction, Action, CancelledActionException, parse_coordinates, is_whole_number
from actions.take import TestAction, TestAction2
from field import RoomItem
from field.node_item import StableItem, PlowedFieldItem

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
        num_stables = 0
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


class PlowFieldAction(Action):
    """
    Plow a single space on the player's field board
    """

    def update(self):
        pass

    def process(self, player, **kwargs):
        player.field.draw()

        correct_input = False
        while not correct_input:
            try:
                coordinates_input = raw_input('Write the coordinates of the field to plow: (eg \'31\' or \'3 1\')')
                if coordinates_input.lower() == 'cancel':
                    raise CancelledActionException()
                x, y = parse_coordinates(coordinates_input)
                player.field.add_item_to_node(x, y, PlowedFieldItem())
                correct_input = True
            except ValueError as e:
                print e.message

        print 'Plowed a field.'
        player.field.draw()

    def describe(self):
        return 'Plow a single space in your field.'


class SowFieldAction(Action):
    """
    Sow a plowed field on the player's field board
    """

    def update(self):
        pass

    def _is_node_valid(self, node):
        if node.item:
            if not isinstance(node.item, PlowedFieldItem):
                raise ValueError('The selected field is not plowed')
            if node.item.has_resources:
                raise ValueError('The selected field is already sown')
            return True
        raise ValueError('The selected field is not plowed')

    def _select_field_node(self, player):
        node = None
        valid_node = False
        while not valid_node:
            coordinates_input = raw_input('Write the coordinates of the field to sow: (eg \'31\' or \'3 1\')')
            if coordinates_input.lower() == 'cancel':
                raise CancelledActionException()
            x, y = parse_coordinates(coordinates_input)

            # make them select a field node
            try:
                node = player.field.get_node_by_coordinate(x, y)
                valid_node = self._is_node_valid(node)
            except ValueError as e:
                print e.message

        return node

    def _select_crop_to_sow(self, player):
        print "You have %s grain and %s vegetables, what type of crop do you wish to sow?" % \
              (player.grain, player.vegetable)

        crop = None
        while not crop:
            input_crop = raw_input('Write the coordinates of the type of crop to sow: (eg \'grain\' or \'vegetable\')')
            if input_crop == 'cancel':
                raise CancelledActionException()
            elif input_crop.strip() in ['grain', 'vegetable']:
                return input_crop.strip()
            else:
                print "%s is not a valid crop type" % input_crop

    def _determine_required_grains_and_vegetables(self, crop):
        grain = 0
        vegetable = 0
        if crop == 'grain':
            grain += 1
        if crop == 'vegetable':
            vegetable += 1

        return grain, vegetable

    def _sow_crop(self, player, node, grain, vegetables):
        if grain > 0:
            if player.grain > 0:
                node.item.grain += 3
                player.grain -= 1
            else:
                raise ValueError("You don't have enough grain to sow a field.")
        elif vegetables > 0:
            if player.vegetable > 0:
                node.item.vegetable += 2
                player.vegetable -= 1
            else:
                raise ValueError("You don't have enough vegetables to sow a field.")

    def process(self, player, **kwargs):
        player.field.draw()

        finished_sowing = False
        while not finished_sowing:
            try:
                next_node_to_sow = self._select_field_node(player)
                crop_to_sow = self._select_crop_to_sow(player)
                grain, vegetables = self._determine_required_grains_and_vegetables(crop_to_sow)
                self._sow_crop(player, next_node_to_sow, grain, vegetables)
            except ValueError as e:
                print e.message
                continue

            finished_input = raw_input('Type \'more\' to sow another field, type anything else to end this action')
            finished_sowing = finished_input.strip() != 'more'

    def describe(self):
        return 'Sow one or more plowed fields.'


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