import logging
import sys
from actions import CancelledActionException
from game_board import GameBoard
from player import Player

__author__ = 'djw'


class Game(object):
    """
    Responsible for managing the flow of a game and all of its entities.
    """
    def __init__(self):
        # set up game parameters and initialize data structures
        logging.debug('initializing')
        self.player = Player()
        self.game_board = GameBoard()

    # The current round of play
    current_round = 1

    # The number of rounds played before the game ends
    GAME_LENGTH = 14

    def run(self):
        # execute the iterative flow of the game
        while self.current_round <= self.GAME_LENGTH:
            self.player.update()
            self.game_board.update()
            print 'Round: %s' % self.current_round
            while self.player.has_idle_family_members:
                action = self.get_action_input()
                if not self.game_board.available_actions[action].is_occupied:
                    try:
                        self.game_board.available_actions[action].take(self.player)
                    except CancelledActionException:
                        continue
                    self.player.send_family_member_to_work()
                else:
                    print 'The %s space is already occupied. Type -a to see the board.' % action
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

    def get_action_input(self):
        action_input = raw_input('Please type an action: ').lower()
        if action_input in self.game_board.available_actions.keys():
            return action_input
        elif action_input == 'player':
            self.player.draw()
        elif action_input == 'field':
            self.player.field.draw()
        elif action_input == '-a':
            self.game_board.draw()
        else:
            print 'invalid action: %s' % action_input
            print 'type -a to see a list of available actions'
        return self.get_action_input()


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