import pygame
from settings import *

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((20, 20))
        if self.type == "speed": self.image.fill(ITEM_BLUE)
        elif self.type == "jump": self.image.fill(ITEM_GOLD)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))