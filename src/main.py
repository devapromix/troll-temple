import sys

from game import Game

if __name__ == '__main__':
    wizard = 'wizard' in sys.argv
    Game(wizard).play()
