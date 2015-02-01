import logging
import sys
from plyr import Player

__author__ = 'djw'


class Game(object):
    """
    Responsible for managing the flow of a game and all of its entities.
    """
    def __init__(self):
        # set up game parameters and initialize data structures
        logging.debug('initializing')
        self.player = Player()

    # The current round of play
    current_round = 1

    # The number of rounds played before the game ends
    GAME_LENGTH = 14

    def run(self):
        # execute the iterative flow of the game
        while self.current_round <= self.GAME_LENGTH:
            self.player.update()
            print 'Round: %s' % self.current_round
            self.current_round += 1
        self.end()

    def end(self):
        # calculate score, print results
        score = self.calculate_final_score()
        print 'Your score was: %s' % score

    def calculate_final_score(self):
        # calculate the plyr's final score
        logging.debug('calculating final score for plyr')
        score = 0  # get stuff here
        return score


# !ENTRY POINT!
if __name__ == "__main__":
    # set up logging
    log_level = logging.CRITICAL
    if len(sys.argv) == 2 and sys.argv[1] == '-d':
            log_level = logging.DEBUG
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    # run game
    game = Game()
    game.run()