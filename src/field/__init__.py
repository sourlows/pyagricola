from pygraph.classes.graph import graph
__author__ = 'Eliniel'
"""
Classes and methods that control the behaviour of a playing field
"""


class FieldNode(object):
    def __init__(self, label, item=None):
        self.label = label
        self.item = item

    def update(self):
        """ Called at the beginning of each turn """
        if self.item:
            self.item.update()


class Field(object):

    def __init__(self):
        self.field = graph()
        self.matrix = [[0 for x in xrange(7)] for x in xrange(5)]
        
        # Create field nodes in graph
        for y in xrange(0, 5):
            for x in xrange(0, 7):
                index_string = '%s%s' % (y, x)
                node = FieldNode(label=index_string)
                self.field.add_node(node)
                self.matrix[y][x] = node

        # Horizontal edges
        for y in xrange(0, 5):
            for x in xrange(0, 6):
                self.field.add_edge((self.matrix[y][x], self.matrix[y][x+1]))

        # Vertical edges
        for x in xrange(0, 7):
            for y in xrange(0, 4):
                self.field.add_edge((self.matrix[y][x], self.matrix[y+1][x]))