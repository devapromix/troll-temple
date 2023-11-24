from common.utils import random_by_level
from mobs.mobs import *


if __name__ == '__main__':
    d = [random_by_level(12, Monster.ALL)().name for i in range(20)]
    print('\n'.join(d))
