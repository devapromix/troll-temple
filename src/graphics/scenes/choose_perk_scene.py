from mobs.perks.perks import *


class ChoosePerkScene:
    def __init__(self, player):
        self.__player = player
        self.perks = player.perks.generate_new_perks()

    def show(self):
        self.__draw()
        perk = self.__select_item()
        if perk is not None:
            self.__player.perks.teach(perk)

    def __select_item(self):
        from common.game import readkey, pygame
        while True:
            key = readkey()
            if key in range(pygame.K_a, pygame.K_z):
                i = key - pygame.K_a
                if 0 <= i < len(self.perks):
                    return self.perks[i]
            if key in [pygame.K_ESCAPE]:
                return None

    def __draw(self):
        from common.game import clear, refresh, out, COLOR_ITEM
        clear()
        out(10, 1, "It's a time to choose your destiny", COLOR_ITEM)
        for i, perk in enumerate(self.perks):
            id = chr(i + ord('a'))
            out(3, i + 3, id, COLOR_ITEM)
            out(5, i + 3, perk.name, COLOR_ITEM)
        refresh()
