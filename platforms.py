import pygame
from settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=PLATFORM_GRAY, move_x=0, speed=2):
        super().__init__()
        self.image = pygame.Surface((width, height))
        
        if move_x > 0:
            self.image.fill(MOVING_PLATFORM_COLOR)
        else:
            self.image.fill(color)
            
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x = x
        self.move_dist = move_x
        self.speed = speed
        self.direction = 1

    def update(self):
        if self.move_dist > 0:
            self.rect.x += self.speed * self.direction
            if self.rect.x > self.start_x + self.move_dist:
                self.direction = -1
            elif self.rect.x < self.start_x:
                self.direction = 1

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))