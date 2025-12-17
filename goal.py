import pygame
from settings import *


class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # try to load an exit image; fall back to simple green rectangle
        img = None
        try:
            img = pygame.image.load("assets/exit.png").convert_alpha()
            # expand the image: make it wider while preserving aspect ratio
            iw, ih = img.get_size()
            target_w = 40
            scale = target_w / float(max(1, iw))
            new_h = max(1, int(ih * scale))
            img = pygame.transform.smoothscale(img, (target_w, new_h))
        except Exception:
            img = None

        if img:
            self.image = img
        else:
            # fallback: wider green door
            self.image = pygame.Surface((40, 100))
            self.image.fill(FLAG_GREEN)

        self.rect = self.image.get_rect(bottomleft=(x, y))

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))