import pygame
from settings import *

# Slightly darker blue for visibility against light backgrounds
DARK_BLUE = (0, 40, 180)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            img = pygame.image.load("assets/player.jpg")
            img = pygame.transform.scale(img, (30, 40))
            self.image = img.convert_alpha()
            self.has_image = True
        except Exception:
            self.image = pygame.Surface((30, 40))
            self.image.fill(BRICK_RED)
            self.has_image = False
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
        self.on_ground = False
        self.is_alive = True
        self.speed_boost = 0
        self.jump_boost = 0
        self.current_platform = None

    def update(self, keys, platforms):
        dx = 0
        dy = 0
        
        current_speed = PLAYER_SPEED + self.speed_boost
        current_jump = JUMP_STRENGTH + self.jump_boost

        if keys[pygame.K_LEFT]: dx = -current_speed
        if keys[pygame.K_RIGHT]: dx = current_speed
        
        if self.on_ground and self.current_platform:
            if self.current_platform.move_dist > 0:
                dx += self.current_platform.speed * self.current_platform.direction

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = current_jump
            self.on_ground = False
            self.current_platform = None

        self.velocity_y += GRAVITY
        dy += self.velocity_y

        self.rect.x += dx
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dx > 0: self.rect.right = platform.rect.left
                elif dx < 0: self.rect.left = platform.rect.right

        self.rect.y += dy
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.current_platform = platform
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

        if self.rect.y > SCREEN_HEIGHT + 100:
            self.is_alive = False

    def merge_with_item(self, item_type):
        if item_type == "speed":
            self.speed_boost = 5
            if not getattr(self, 'has_image', False):
                self.image.fill(ITEM_BLUE)
        elif item_type == "jump":
            self.jump_boost = -5
            if not getattr(self, 'has_image', False):
                self.image.fill(ITEM_GOLD)

    def draw(self, surface, camera_x):
        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y
        # Strong layered blue glow for speed boost (use darker tint for contrast)
        if getattr(self, 'speed_boost', 0) > 0:
            w, h = self.rect.size
            layers = [ (w+44, h+44, 80), (w+30, h+30, 140), (w+18, h+18, 220) ]
            for sw, sh, alpha in layers:
                glow = pygame.Surface((sw, sh), pygame.SRCALPHA)
                pygame.draw.ellipse(glow, (*DARK_BLUE, alpha), glow.get_rect())
                surface.blit(glow, (draw_x - (sw-w)//2, draw_y - (sh-h)//2), special_flags=pygame.BLEND_ADD)
        # Strong layered gold glow for jump boost
        if getattr(self, 'jump_boost', 0) != 0:
            w, h = self.rect.size
            layers2 = [ (w+50, h+50, 70), (w+34, h+34, 130), (w+20, h+20, 210) ]
            for sw, sh, alpha in layers2:
                glow2 = pygame.Surface((sw, sh), pygame.SRCALPHA)
                pygame.draw.ellipse(glow2, (*ITEM_GOLD, alpha), glow2.get_rect())
                surface.blit(glow2, (draw_x - (sw-w)//2, draw_y - (sh-h)//2), special_flags=pygame.BLEND_ADD)
        surface.blit(self.image, (draw_x, draw_y))