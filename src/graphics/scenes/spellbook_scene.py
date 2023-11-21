import pygame
from common.game import out
from graphics.scenes.selection_scene import SelectionScene

class SpellbookScene(SelectionScene):
    def __init__(self, player):
        super().__init__("SPELLBOOK Press [ENTER] to read spell, [ESC] to exit", player.spells, True)
        self.has_footer = False
        self.player = player

    def _draw_item_name(self, x: int, y: int, spell: object) -> None:
        out(x, y, spell.descr, spell.color)

    def _check_input(self, key: int) -> bool:
        if super()._check_input(key, False):
            return True
            
        if key == pygame.K_RETURN:
            if self.focusable:
                spell = self.selected
                if spell:
                    self.player.use_spell(spell)
                    self.exit()
            return True
        
        if key == pygame.K_ESCAPE:
            self.exit()
            return True
        
        return False
            