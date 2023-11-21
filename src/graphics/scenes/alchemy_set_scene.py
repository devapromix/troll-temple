import pygame
from common.game import out
from graphics.scenes.selection_scene import SelectionScene

class AlchemySetScene(SelectionScene):
    def __init__(self, player):
        super().__init__("ALCHEMYSET Press [ENTER] to create, [ESC] to exit", player.recipes, True)
        self.player = player

    def _draw_item_name(self, x: int, y: int, recipe: object) -> None:
        out(x, y, recipe.descr, recipe.color)

    def _check_input(self, key: int) -> bool:
        if super()._check_input(key, False):
            return True
            
        if key == pygame.K_RETURN:
            if self.focusable:
                recipe = self.selected
                if recipe:
                    self.player.create(recipe)
                    self.exit()
            return True
        
        if key == pygame.K_ESCAPE:
            self.exit()
            return True
        
        return False
            