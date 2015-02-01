import logging

__author__ = 'djw'


class Game(object):
    """
    Responsible for managing the flow of a game and all of its entities.
    """
    def __init__(self):
        # set up game parameters and initialize data structures
        logging.debug('initializing')

    # The current round of play
    current_round = 1

    # The number of rounds played before the game ends
    GAME_LENGTH = 15

    def run(self):
        # execute the iterative flow of the game
        while self.current_round < 15:
            print 'Round: %s' % self.current_round
            self.current_round += 1
        self.end()

    def end(self):
        # calculate score, print results
        score = self.calculate_final_score()
        print 'Your score was: %s' % score

    def calculate_final_score(self):
        # calculate the player's final score
        logging.debug('calculating final score for player')
        score = 0  # get stuff here
        return score



# start everything!
if __name__ == "__main__":
    game = Game()
    game.run()