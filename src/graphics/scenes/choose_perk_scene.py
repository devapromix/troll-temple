from graphics.scenes.selection_scene import SelectionScene
from mobs.perks.perks import *


class ChoosePerkScene(SelectionScene):
    def __init__(self, player):
        super().__init__("Choose your destiny", player.perks.generate_new_perks())
        self.__player = player

    def show(self):
        super().show()
        self.__player.perks.teach(self.selected)
