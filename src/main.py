import sys

from common.game_class import Game

if __name__ == '__main__':
    wizard = 'wizard' in sys.argv
    Game(True).play()
