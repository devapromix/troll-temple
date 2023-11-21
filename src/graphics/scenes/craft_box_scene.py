import pygame
from common.game import out
from graphics.scenes.selection_scene import SelectionScene

class CraftBoxScene(SelectionScene):
    def __init__(self, player):
        super().__init__("CRAFT BOX Press [ENTER] to craft an item, [ESC] to exit", player.plans, True)
        self.player = player
        self.has_footer = False

    def _draw_item_name(self, x: int, y: int, plan: object) -> None:
        out(x, y, plan.descr, plan.color)

    def _check_input(self, key: int) -> bool:
        if super()._check_input(key, False):
            return True
            
        if key == pygame.K_RETURN:
            if self.focusable:
                plan = self.selected
                if plan:
                    self.player.craft(plan)
                    self.exit()
            return True
        
        if key == pygame.K_ESCAPE:
            self.exit()
            return True
        
        return False
            