import field
from field.node_item import RoomItem, StableItem
from pygraph.classes.graph import graph
__author__ = 'Eliniel'
"""
Classes and methods that control the behaviour of a playing field
"""


class FieldNode(object):
    """
    A single space on a field board, possibly holding a room/stable/plowed field
    """
    def __init__(self, label, item=None):
        self.label = label
        self.item = item

    def update(self):
        """ Called at the beginning of each turn """
        if self.item:
            self.item.update()

    def describe(self):
        if not self.item:
            return 'e'
        else:
            #print 'drawing node %s' % self.label
            return self.item.describe()


class Field(graph):
    """
    The game board that represents the player's field upon which he may build items in each cell
    """
    def __init__(self):
        super(Field, self).__init__()
        self.index_matrix = [[0 for x in xrange(7)] for x in xrange(5)]

        # Create field nodes in graph
        for y in xrange(0, 5):
            for x in xrange(0, 7):
                index_string = '%s%s' % (y, x)
                node = FieldNode(label=index_string)
                self.add_node(node)
                self.index_matrix[y][x] = node

        # Horizontal edges
        for y in xrange(0, 5):
            for x in xrange(0, 6):
                self.add_edge((self.index_matrix[y][x], self.index_matrix[y][x+1]))

        # Vertical edges
        for x in xrange(0, 7):
            for y in xrange(0, 4):
                self.add_edge((self.index_matrix[y][x], self.index_matrix[y+1][x]))

        # build initial rooms
        self.index_matrix[1][1].item = RoomItem()
        self.index_matrix[2][1].item = RoomItem()

    @property
    def room_material(self):
        # all nodes with room must have the same material type
        for node in self.nodes():
            if node.item and hasattr(node.item, 'material'):
                # so just return the first one we find
                return node.item.material
        return None

    def get_node_by_coordinate(self, x, y):
        if not self.index_matrix[y][x]:
            raise ValueError('Invalid coordinates %s %s' % (x, y))
        return self.index_matrix[y][x]

    def add_item_to_node(self, x, y, item):
        if not 1 <= x <= 5 or not 1 <= y <= 3:
            raise ValueError('The coordinates x: %s, y: %s were invalid. '
                             'X must be between 1 and 5, Y must be between 1 and 3' % (x, y))
        if self.index_matrix[y][x].item:
            raise ValueError('The tile at %s %s is already occupied.' % (x, y))
        self.index_matrix[y][x].item = item

    def draw(self):
        for y in xrange(1, 4):
            # write out each row of nodes on a separate line
            desc = ""
            for x in xrange(1, 6):
                desc += self.index_matrix[y][x].describe()
            print desc

    def update_node_animals(self, x, y, animal, count):
        if not 1 <= x <= 5 or not 1 <= y <= 3:
            raise ValueError('The coordinates x: %s, y: %s were invalid. '
                            'X must be between 1 and 5, Y must be between 1 and 3' % (x, y))
        if self.index_matrix[y][x].item is None:
            raise ValueError('Animals can only be placed in rooms, fenced pastures, or stables.')

        if isinstance(self.index_matrix[y][x].item, RoomItem):
            max_animals = 1
            if count > max_animals or self.index_matrix[y][x].item.sheep == int(1) \
                    or self.index_matrix[y][x].item.boars == int(1) \
                    or self.index_matrix[y][x].item.cattle == int(1):
                raise ValueError('You can only hold one animal in a room')
            self.index_matrix[y][x].item.update_animals(animal, count)
        if isinstance(self.index_matrix[y][x].item, StableItem):
            max_animals = 1
            # Logic for fences to be added here later;
            # Currently only the case of an unfenced stable is considered
            if count > max_animals or self.index_matrix[y][x].item.sheep == int(1) \
                    or self.index_matrix[y][x].item.boars == int(1) \
                    or self.index_matrix[y][x].item.cattle == int(1):
                raise ValueError('You can only hold one animal in a room')
            self.index_matrix[y][x].item.update_animals(animal, count)

    def update_node_crops(self, x, y, crop, count):
        if not 1 <= x <= 5 or not 1 <= y <= 3:
            raise ValueError('The coordinates x: %s, y: %s were invalid. '
                            'X must be between 1 and 5, Y must be between 1 and 3' % (x, y))
        if self.index_matrix[y][x].item is None:
            raise ValueError('Crops can only be placed in plowed fields.')