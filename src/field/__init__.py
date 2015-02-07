from pygraph.classes.graph import graph
__author__ = 'Eliniel'
"""
Classes and methods that control the behaviour of a playing field
"""

class Field(object):

    def __init__(self):
        self.field = graph()
        
        # Create field nodes in graph
        for y in xrange(0, 5):
            for x in xrange(0, 7):
                index_string = '%s%s' % (y, x)
                self.field.add_node(index_string)

        # Horizontal edges
        for y in xrange(0, 5):
            for x in xrange(0, 6):
                firstnode = '%s%s' % (y, x)
                secondnode = '%s%s' % (y, x+1)
                self.field.add_edge((firstnode, secondnode))

        # Vertical edges
        for x in xrange(0, 7):
            for y in xrange(0, 4):
                firstnode = '%s%s' % (y, x)
                secondnode = '%s%s' % (y+1, x)
                self.field.add_edge((firstnode, secondnode))