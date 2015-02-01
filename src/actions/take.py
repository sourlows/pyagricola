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
        self.current_clay = 0


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
        self.current_reed = 0


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
        self.current_wood = 0