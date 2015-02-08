from field.node_item import RoomItem
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

    def draw(self):
        for y in xrange(1, 4):
            desc = ""
            for x in xrange(1, 6):
                #index_string = '%s%s' % (y, x)
                #node = FieldNode(label=index_string)
                #self.add_node(node)
                desc += self.index_matrix[y][x].describe()
            print desc