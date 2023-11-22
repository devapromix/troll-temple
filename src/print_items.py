from items.items import *

if __name__ == '__main__':
    d = [random_by_level(1, Item.ALL)().descr for i in range(20)]
    print('\n'.join(d))
