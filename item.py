import pygame
from settings import *

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        
        if self.type == "speed":
            self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
            self.image.fill(ITEM_BLUE)
        elif self.type == "jump":
            self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
            self.image.fill(ITEM_GOLD)
        elif self.type == "coin":
            
            self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
            pygame.draw.circle(self.image, ITEM_GOLD, (8, 8), 7)
            pygame.draw.circle(self.image, (220,180,0), (8, 8), 5)
        else:
            self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
            self.image.fill(ITEM_BLUE)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))