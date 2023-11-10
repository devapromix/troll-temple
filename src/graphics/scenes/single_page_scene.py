from ..color import Color
from .scene import Scene
import tcod as T

class SinglePageScene(Scene):
    def __init__(self):
        super().__init__()
        
    def _check_input(self, key: int) -> bool:
        from common.game import pygame
        if key == pygame.K_RETURN:
            self.exit()
            return True
        return False
        
























