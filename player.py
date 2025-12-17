import pygame
import random
import math
from settings import *


DARK_BLUE = (0, 40, 180)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        loaded = False
        for fn in ("assets/player.png", "assets/player.jpg", "assets/player.jpeg"):
            try:
                img = pygame.image.load(fn)
                
                img = pygame.transform.scale(img, (40, 40))
                self.image = img.convert_alpha()
                self.has_image = True
                loaded = True
                break
            except Exception:
                continue
        if not loaded:
            self.image = pygame.Surface((40, 40))
            self.image.fill(BRICK_RED)
            self.has_image = False

        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
        self.on_ground = False
        self.is_alive = True
        self.speed_boost = 0
        self.jump_boost = 0
        self.gold = 0
        self.current_platform = None

        self.death_timer = 0
        self.death_duration = 60
        self.death_started = False
        self.particles = []
        self.glow_phase = 0.0

    def update(self, keys, platforms):
        dx = 0
        dy = 0

        current_speed = PLAYER_SPEED + self.speed_boost
        current_jump = JUMP_STRENGTH + self.jump_boost

        if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx = -current_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx = current_speed

        if self.on_ground and self.current_platform:
            if self.current_platform.move_dist > 0:
                dx += self.current_platform.speed * self.current_platform.direction

        if (keys[pygame.K_w] or keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
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

        if not self.is_alive and not self.death_started:
            self.start_death()

        self.glow_phase += 0.12
        if self.glow_phase > math.tau:
            self.glow_phase -= math.tau

    def start_death(self):
        if self.death_started:
            return
        self.death_started = True
        self.death_timer = 0
        self.particles = []
        max_life = 80
        num = 120
        for _ in range(num):
            px = random.uniform(self.rect.left, self.rect.right)
            py = random.uniform(self.rect.top, self.rect.bottom)
            vx = random.uniform(-4.0, 4.0)
            vy = random.uniform(-6.0, -1.0)
            life = random.randint(40, max_life)
            size = random.randint(2, 4)
            palette = [BRICK_RED, WHITE]
            if getattr(self, 'speed_boost', 0) > 0:
                palette.append(DARK_BLUE)
            if getattr(self, 'jump_boost', 0) != 0:
                palette.append(ITEM_GOLD)
            color = random.choice(palette)
            self.particles.append({'x': px, 'y': py, 'vx': vx, 'vy': vy, 'life': life, 'max_life': life, 'size': size, 'color': color})

    def merge_with_item(self, item_type):
        if item_type == "speed":
            self.speed_boost = 5
            if not getattr(self, 'has_image', False):
                self.image.fill(ITEM_BLUE)
        elif item_type == "jump":
            self.jump_boost = -5
            if not getattr(self, 'has_image', False):
                self.image.fill(ITEM_GOLD)
        elif item_type == "coin":
            try:
                self.gold += 1
            except Exception:
                self.gold = getattr(self, 'gold', 0) + 1

    def draw(self, surface, camera_x):
        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y

        if not self.is_alive:
            if not self.death_started:
                self.start_death()
            self.death_timer += 1
            prog = min(1.0, self.death_timer / max(1, self.death_duration))
            for p in self.particles[:]:
                p['vy'] -= 0.12
                p['x'] += p['vx'] * 0.6
                p['y'] += p['vy']
                p['vx'] *= 0.985
                if p['size'] > 1 and random.random() < 0.02:
                    p['size'] -= 1
                p['life'] -= 1
                if p['life'] <= 0:
                    self.particles.remove(p)
                    continue
            for p in self.particles:
                life_ratio = max(0.0, p['life'] / max(1, p['max_life']))
                a = int(255 * life_ratio)
                s = max(1, int(p['size']))
                surf = pygame.Surface((s * 2, s * 2), pygame.SRCALPHA)
                col = (*p['color'], a)
                pygame.draw.circle(surf, col, (s, s), s)
                surface.blit(surf, (p['x'] - camera_x - s, p['y'] - s))

            w, h = self.rect.size
            scale = max(0.2, 1.0 - 0.8 * prog)
            new_w = max(1, int(w * scale))
            new_h = max(1, int(h * scale))
            img = pygame.transform.smoothscale(self.image, (new_w, new_h))
            angle = prog * 360
            img = pygame.transform.rotate(img, angle)
            alpha = int(255 * (1.0 - prog))
            img.set_alpha(alpha)
            glow_fade = int(200 * (1.0 - prog))
            if getattr(self, 'speed_boost', 0) > 0 and glow_fade > 0:
                gw, gh = img.get_size()
                glow = pygame.Surface((gw + 12, gh + 12), pygame.SRCALPHA)
                pygame.draw.ellipse(glow, (*DARK_BLUE, glow_fade), glow.get_rect())
                surface.blit(glow, (draw_x - (gw+12-w)//2 - 6, draw_y - (gh+12-h)//2 - 6), special_flags=pygame.BLEND_ADD)
            if getattr(self, 'jump_boost', 0) != 0 and glow_fade > 0:
                gw, gh = img.get_size()
                pad = 10
                glow_w, glow_h = gw + pad, gh + pad
                glow2 = pygame.Surface((glow_w, glow_h), pygame.SRCALPHA)
                max_alpha = max(6, int(glow_fade * 0.45))
                steps = 6
                for i in range(steps):
                    t = i / float(steps)
                    a = int(max_alpha * (1.0 - t) * (0.7 + 0.3 * (1 - t)))
                    inset = int(i * (pad / steps))
                    rect = pygame.Rect(inset, inset, glow_w - inset * 2, glow_h - inset * 2)
                    pygame.draw.ellipse(glow2, (*ITEM_GOLD, a), rect)
                surface.blit(glow2, (draw_x - (glow_w-gw)//2, draw_y - (glow_h-gh)//2), special_flags=pygame.BLEND_ADD)
            float_up = int(40 * prog)
            img_x = draw_x + (w - img.get_width()) // 2
            img_y = draw_y - float_up + (h - img.get_height()) // 2
            surface.blit(img, (img_x, img_y))
            return

        if getattr(self, 'speed_boost', 0) > 0:
            w, h = self.rect.size
            layers = [ (w+8, h+8, 110), (w+4, h+4, 70) ]
            for sw, sh, alpha in layers:
                glow = pygame.Surface((sw, sh), pygame.SRCALPHA)
                pygame.draw.ellipse(glow, (*DARK_BLUE, alpha), glow.get_rect())
                surface.blit(glow, (draw_x - (sw-w)//2, draw_y - (sh-h)//2), special_flags=pygame.BLEND_ADD)

        if getattr(self, 'jump_boost', 0) != 0:
            w, h = self.rect.size
            pulse = 1.0 + 0.18 * math.sin(getattr(self, 'glow_phase', 0.0))
            pad_base = 8
            pad = max(2, int(pad_base * pulse))
            glow_w, glow_h = w + pad * 2, h + pad * 2
            halo = pygame.Surface((glow_w, glow_h), pygame.SRCALPHA)
            max_alpha = int(180 * pulse)
            steps = 7
            for i in range(steps):
                t = i / float(steps)
                a = int(max_alpha * (1.0 - t) * (0.35 + 0.65 * (1 - t)))
                inset = int(t * pad)
                rect = pygame.Rect(inset, inset, glow_w - inset * 2, glow_h - inset * 2)
                pygame.draw.ellipse(halo, (*ITEM_GOLD, a), rect)
            surface.blit(halo, (draw_x - (glow_w-w)//2, draw_y - (glow_h-h)//2), special_flags=pygame.BLEND_ADD)

        surface.blit(self.image, (draw_x, draw_y))
import pygame
import random
import math
from settings import *

DARK_BLUE = (0, 40, 180)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        loaded = False
        for fn in ("assets/player.png", "assets/player.jpg", "assets/player.jpeg"):
            try:
                img = pygame.image.load(fn)
                
                img = pygame.transform.scale(img, (40, 40))
                self.image = img.convert_alpha()
                self.has_image = True
                loaded = True
                break
            except Exception:
                continue
        if not loaded:
            self.image = pygame.Surface((40, 40))
            self.image.fill(BRICK_RED)
            self.has_image = False
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
        self.on_ground = False
        self.is_alive = True
        self.speed_boost = 0
        self.jump_boost = 0
        self.gold = 0
        self.current_platform = None

        self.death_timer = 0
        self.death_duration = 60
        self.death_started = False
        self.particles = []
        self.glow_phase = 0.0

    def update(self, keys, platforms):
        dx = 0
        dy = 0

        current_speed = PLAYER_SPEED + self.speed_boost
        current_jump = JUMP_STRENGTH + self.jump_boost

        if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx = -current_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx = current_speed

        if self.on_ground and self.current_platform:
            if self.current_platform.move_dist > 0:
                dx += self.current_platform.speed * self.current_platform.direction

        if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
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

        if not self.is_alive and not self.death_started:
            self.start_death()

        self.glow_phase += 0.12
        if self.glow_phase > math.tau:
            self.glow_phase -= math.tau

    def start_death(self):
        self.death_started = True
        self.death_timer = 0
        self.particles = []
        max_life = 80
        num = 120
        for _ in range(num):
            px = random.uniform(self.rect.left, self.rect.right)
            py = random.uniform(self.rect.top, self.rect.bottom)
            vx = random.uniform(-4.0, 4.0)
            vy = random.uniform(-6.0, -1.0)
            life = random.randint(40, max_life)
            size = random.randint(2, 4)
            palette = [BRICK_RED, WHITE]
            if getattr(self, 'speed_boost', 0) > 0:
                palette.append(DARK_BLUE)
            if getattr(self, 'jump_boost', 0) != 0:
                palette.append(ITEM_GOLD)
            color = random.choice(palette)
            self.particles.append({'x': px, 'y': py, 'vx': vx, 'vy': vy, 'life': life, 'max_life': life, 'size': size, 'color': color})
            self.on_ground = False
            self.is_alive = True
            self.speed_boost = 0
            self.jump_boost = 0
            self.gold = 0
            self.current_platform = None

            self.death_timer = 0
            self.death_duration = 60
            self.death_started = False
            self.particles = []

        def update(self, keys, platforms):
            dx = 0
            dy = 0

            current_speed = PLAYER_SPEED + self.speed_boost
            current_jump = JUMP_STRENGTH + self.jump_boost

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx = -current_speed
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx = current_speed

            if self.on_ground and self.current_platform:
                if self.current_platform.move_dist > 0:
                    dx += self.current_platform.speed * self.current_platform.direction

            if (keys[pygame.K_w] or keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
                self.velocity_y = current_jump
                self.on_ground = False
                self.current_platform = None

            self.velocity_y += GRAVITY
            dy += self.velocity_y

            self.rect.x += dx
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if dx > 0:
                        self.rect.right = platform.rect.left
                    elif dx < 0:
                        self.rect.left = platform.rect.right

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

            if not self.is_alive and not self.death_started:
                self.start_death()

    def start_death(self):
        self.death_started = True
        self.death_timer = 0
        self.particles = []
        max_life = 80
        DARK_BLUE = (0, 40, 180)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            img = pygame.image.load("assets/player.png")
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
        self.gold = 0
        self.current_platform = None

        self.death_timer = 0
        self.death_duration = 60
        self.death_started = False
        self.particles = []

    def update(self, keys, platforms):
        dx = 0
        dy = 0

        current_speed = PLAYER_SPEED + self.speed_boost
        current_jump = JUMP_STRENGTH + self.jump_boost

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -current_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = current_speed

        if self.on_ground and self.current_platform:
            if self.current_platform.move_dist > 0:
                dx += self.current_platform.speed * self.current_platform.direction

        if (keys[pygame.K_w] or keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.velocity_y = current_jump
            self.on_ground = False
            self.current_platform = None

        self.velocity_y += GRAVITY
        dy += self.velocity_y

        self.rect.x += dx
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dx > 0:
                    self.rect.right = platform.rect.left
                elif dx < 0:
                    self.rect.left = platform.rect.right

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

        if not self.is_alive and not self.death_started:
            self.start_death()

    def start_death(self):
        self.death_started = True
        self.death_timer = 0
        self.particles = []
        max_life = 80
        num = 120
        for _ in range(num):
            px = random.uniform(
                self.rect.left, self.rect.right)
            py = random.uniform(
                self.rect.top, self.rect.bottom)
            vx = random.uniform(-4.0, 4.0)
            vy = random.uniform(-6.0, -1.0)
            life = random.randint(40, max_life)
            size = random.randint(2, 4)
            palette = [BRICK_RED, WHITE]
            if getattr(self, 'speed_boost', 0) > 0:
                palette.append(DARK_BLUE)
            if getattr(self, 'jump_boost', 0) != 0:
                palette.append(ITEM_GOLD)
            color = random.choice(palette)
            self.particles.append(
                {'x': px, 'y': py, 'vx': vx, 'vy': vy, 'life': life, 'max_life': life, 'size': size, 'color': color})

    def merge_with_item(self, item_type):
        if item_type == "speed":
            self.speed_boost = 5
            if not getattr(self, 'has_image', False):
                self.image.fill(ITEM_BLUE)
        elif item_type == "jump":
            self.jump_boost = -5
            if not getattr(self, 'has_image', False):
                self.image.fill(ITEM_GOLD)
        elif item_type == "coin":
            try:
                self.gold += 1
            except Exception:
                self.gold = getattr(self, 'gold', 0) + 1
    def merge_with_item(self, item_type):
        if item_type == "speed":
            self.speed_boost = 5
            if not getattr(self, 'has_image', False):
                self.image.fill(ITEM_BLUE)
        elif item_type == "jump":
            self.jump_boost = -5
            if not getattr(self, 'has_image', False):
                self.image.fill(ITEM_GOLD)
        elif item_type == "coin":
            try:
                self.gold += 1
            except Exception:
                self.gold = getattr(self, 'gold', 0) + 1

    def draw(self, surface, camera_x):
        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y
    def draw(self, surface, camera_x):
        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y

        if not self.is_alive:
            if not self.death_started:
                self.start_death()
            self.death_timer += 1
            prog = min(1.0, self.death_timer /
                       max(1, self.death_duration))
            for p in self.particles[:]:
                p['vy'] -= 0.12
                p['x'] += p['vx'] * 0.6
                p['y'] += p['vy']
                p['vx'] *= 0.985
                if p['size'] > 1 and random.random() < 0.02:
                    p['size'] -= 1
                p['life'] -= 1
                if p['life'] <= 0:
                    self.particles.remove(p)
                    continue
            for p in self.particles:
                life_ratio = max(
                    0.0, p['life'] / max(1, p['max_life']))
                a = int(255 * life_ratio)
                s = max(1, int(p['size']))
                surf = pygame.Surface(
                    (s * 2, s * 2), pygame.SRCALPHA)
                col = (*p['color'], a)
                pygame.draw.circle(surf, col, (s, s), s)
                surface.blit(
                    surf, (p['x'] - camera_x - s, p['y'] - s))

            w, h = self.rect.size
            scale = max(0.2, 1.0 - 0.8 * prog)
            new_w = max(1, int(w * scale))
            new_h = max(1, int(h * scale))
            img = pygame.transform.smoothscale(
                self.image, (new_w, new_h))
            angle = prog * 360
            img = pygame.transform.rotate(img, angle)
            alpha = int(255 * (1.0 - prog))
            img.set_alpha(alpha)
            glow_fade = int(200 * (1.0 - prog))
            if getattr(self, 'speed_boost', 0) > 0 and glow_fade > 0:
                gw, gh = img.get_size()
                glow = pygame.Surface(
                    (gw + 12, gh + 12), pygame.SRCALPHA)
                pygame.draw.ellipse(
                    glow, (*DARK_BLUE, glow_fade), glow.get_rect())
                surface.blit(glow, (draw_x - (gw+12-w)//2 - 6, draw_y -
                             (gh+12-h)//2 - 6), special_flags=pygame.BLEND_ADD)
            if getattr(self, 'jump_boost', 0) != 0 and glow_fade > 0:
                gw, gh = img.get_size()
                
                pad = 10
                glow_w, glow_h = gw + pad, gh + pad
                glow2 = pygame.Surface(
                    (glow_w, glow_h), pygame.SRCALPHA)
                max_alpha = max(6, int(glow_fade * 0.45))
                steps = 6
                for i in range(steps):
                    t = i / float(steps)
                    a = int(max_alpha * (1.0 - t)
                            * (0.7 + 0.3 * (1 - t)))
                    inset = int(i * (pad / steps))
                    rect = pygame.Rect(
                        inset, inset, glow_w - inset * 2, glow_h - inset * 2)
                    pygame.draw.ellipse(
                        glow2, (*ITEM_GOLD, a), rect)
                surface.blit(
                    glow2, (draw_x - (glow_w-gw)//2, draw_y - (glow_h-gh)//2), special_flags=pygame.BLEND_ADD)
            float_up = int(40 * prog)
            img_x = draw_x + (w - img.get_width()) // 2
            img_y = draw_y - float_up + \
                (h - img.get_height()) // 2
            surface.blit(img, (img_x, img_y))
            return

        
        if getattr(self, 'speed_boost', 0) > 0:
            w, h = self.rect.size
            layers = [(w+8, h+8, 110), (w+4, h+4, 70)]
            for sw, sh, alpha in layers:
                glow = pygame.Surface(
                    (sw, sh), pygame.SRCALPHA)
                pygame.draw.ellipse(
                    glow, (*DARK_BLUE, alpha), glow.get_rect())
                surface.blit(
                    glow, (draw_x - (sw-w)//2, draw_y - (sh-h)//2), special_flags=pygame.BLEND_ADD)

        if getattr(self, 'jump_boost', 0) != 0:
            w, h = self.rect.size
            
            pad = 8
            glow_w, glow_h = w + pad * 2, h + pad * 2
            halo = pygame.Surface(
                (glow_w, glow_h), pygame.SRCALPHA)
            max_alpha = 180
            steps = 7
            for i in range(steps):
                t = i / float(steps)
                a = int(max_alpha * (1.0 - t) *
                        (0.35 + 0.65 * (1 - t)))
                inset = int(t * pad)
                rect = pygame.Rect(
                    inset, inset, glow_w - inset * 2, glow_h - inset * 2)
                pygame.draw.ellipse(
                    halo, (*ITEM_GOLD, a), rect)
            surface.blit(
                halo, (draw_x - (glow_w-w)//2, draw_y - (glow_h-h)//2), special_flags=pygame.BLEND_ADD)

        surface.blit(self.image, (draw_x, draw_y))
