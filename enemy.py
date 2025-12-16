import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, distance):
        super().__init__()
        try:
            img = pygame.image.load("assets/villain.png")
            img = pygame.transform.scale(img, (30, 30))
            base = img.convert_alpha()
            self.has_image = True
        except Exception:
            base = pygame.Surface((30, 30), pygame.SRCALPHA)
            base.fill(ENEMY_PURPLE)
            # simple eyes so the fallback has a face that can flip
            pygame.draw.circle(base, (255, 255, 255), (8, 10), 3)
            pygame.draw.circle(base, (255, 255, 255), (22, 10), 3)
            pygame.draw.circle(base, (0, 0, 0), (8, 10), 1)
            pygame.draw.circle(base, (0, 0, 0), (22, 10), 1)
            self.has_image = False
        self.base_image = base
        self.image = self.base_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.facing = 1
        self.start_x = x
        self.distance = distance
        self.direction = 1 

    def update(self):
        self.rect.x += self.direction * ENEMY_SPEED
        if self.rect.x > self.start_x + self.distance:
            self.direction = -1
        elif self.rect.x < self.start_x:
            self.direction = 1

        # Flip image when direction changes so the face looks toward movement
        if self.direction != getattr(self, 'facing', 1):
            self.facing = self.direction
            if self.facing < 0:
                self.image = pygame.transform.flip(self.base_image, True, False)
            else:
                self.image = self.base_image

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))