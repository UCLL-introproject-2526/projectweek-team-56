import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, distance):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(ENEMY_PURPLE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x = x
        self.distance = distance
        self.direction = 1 

    def update(self):
        self.rect.x += self.direction * ENEMY_SPEED
        if self.rect.x > self.start_x + self.distance:
            self.direction = -1
        elif self.rect.x < self.start_x:
            self.direction = 1

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))