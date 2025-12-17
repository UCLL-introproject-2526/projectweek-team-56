import pygame
import random
import math
from settings import *


_death_sfx = None


def _remove_bg_by_color(surface, sample_pos=(0, 0), thresh=60):
    """Return a copy of `surface` with pixels similar to the sampled color made transparent.

    This is a simple background remover useful for JPGs where a solid background
    was used. It samples `sample_pos` (default top-left) and makes pixels whose
    squared distance to that color is below `thresh` transparent.
    """
    surf = surface.convert_alpha()
    w, h = surf.get_size()
    try:
        bg = surf.get_at(sample_pos)[:3]
    except Exception:
        bg = (255, 255, 255)
    out = pygame.Surface((w, h), pygame.SRCALPHA)
    thr2 = thresh * thresh
    for x in range(w):
        for y in range(h):
            r, g, b, a = surf.get_at((x, y))
            dr = r - bg[0]
            dg = g - bg[1]
            db = b - bg[2]
            if dr * dr + dg * dg + db * db <= thr2:
                continue
            out.set_at((x, y), (r, g, b, a))
    return out


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
        self.death_started = False
        self.death_timer = 0
        self.death_duration = 50
        self.particles = []

    def update(self):
        if self.death_started:
            self.death_timer += 1
            for p in self.particles[:]:
                p['vy'] += 0.15
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['life'] -= 1
                if p['life'] <= 0:
                    self.particles.remove(p)
            if self.death_timer > self.death_duration:
                super().kill()
            return

        self.rect.x += self.direction * ENEMY_SPEED
        if self.rect.x > self.start_x + self.distance:
            self.direction = -1
        elif self.rect.x < self.start_x:
            self.direction = 1

        if self.direction != getattr(self, 'facing', 1):
            self.facing = self.direction
            if self.facing < 0:
                self.image = pygame.transform.flip(
                    self.base_image, True, False)
            else:
                self.image = self.base_image

    def draw(self, surface, camera_x):
        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y
        if self.death_started:
            for p in self.particles:
                pygame.draw.circle(surface, p['color'], (int(
                    p['x'] - camera_x), int(p['y'])), p['size'])

            prog = min(1.0, self.death_timer / max(1, self.death_duration))
            w, h = self.base_image.get_size()
            scale = max(0.1, 1.0 - 0.9 * prog)
            new_w = max(1, int(w * scale))
            new_h = max(1, int(h * scale))
            img = pygame.transform.smoothscale(self.base_image, (new_w, new_h))
            alpha = int(255 * (1.0 - prog))
            img.set_alpha(alpha)
            img_x = draw_x + (w - new_w) // 2
            img_y = draw_y + (h - new_h) // 2
            surface.blit(img, (img_x - camera_x, img_y))
            return

        surface.blit(self.image, (draw_x, draw_y))

    def start_death(self):
        if self.death_started:
            return
        self.death_started = True
        self.death_timer = 0
        self.particles = []
        global _death_sfx
        try:
            if _death_sfx is None:
                for fname in ("music/enemy_death.mp3", "music/enemy_death.wav", "music/death.wav", "assets/death.wav"):
                    try:
                        _death_sfx = pygame.mixer.Sound(fname)
                        break
                    except Exception:
                        continue
            if _death_sfx:
                try:
                    _death_sfx.play()
                except Exception:
                    pass
        except Exception:
            pass
        num = 30
        for _ in range(num):
            px = random.uniform(self.rect.left, self.rect.right)
            py = random.uniform(self.rect.top, self.rect.bottom)
            vx = random.uniform(-3.0, 3.0)
            vy = random.uniform(-5.0, -1.0)
            life = random.randint(20, 40)
            size = random.randint(2, 4)
            color = random.choice([ENEMY_PURPLE, (255, 255, 255)])
            self.particles.append(
                {'x': px, 'y': py, 'vx': vx, 'vy': vy, 'life': life, 'size': size, 'color': color})


class FlyingEnemy(Enemy):
    """A flying enemy that uses assets/flyer.png and bobs vertically while patrolling."""

    def __init__(self, x, y, distance, amplitude=20, osc_speed=0.12):
        super().__init__(x, y, distance)
        
        loaded = False
        for fname in ("assets/flyer.png", "assets/flyer.jpg", "assets/flyer.jpeg"):
            try:
                img = pygame.image.load(fname)
                img = pygame.transform.scale(img, (36, 24))
                
                if fname.lower().endswith(('.jpg', '.jpeg')):
                    img = _remove_bg_by_color(
                        img, sample_pos=(0, 0), thresh=60)
                else:
                    img = img.convert_alpha()
                self.base_image = img
                self.has_image = True
                loaded = True
                break
            except Exception:
                continue
        if not loaded:
            
            pass
        self.image = self.base_image

        
        self.base_y = y
        self.osc_amplitude = amplitude
        self.osc_speed = osc_speed
        self._osc_t = random.uniform(0, 2 * math.pi)

    def update(self):
        
        if self.death_started:
            super().update()
            return

        
        self.rect.x += self.direction * ENEMY_SPEED
        if self.rect.x > self.start_x + self.distance:
            self.direction = -1
        elif self.rect.x < self.start_x:
            self.direction = 1

       
        self._osc_t += self.osc_speed
        bob = math.sin(self._osc_t) * self.osc_amplitude
        self.rect.y = int(self.base_y + bob)

      
        if self.direction != getattr(self, 'facing', 1):
            self.facing = self.direction
            if self.facing < 0:
                self.image = pygame.transform.flip(
                    self.base_image, True, False)
            else:
                self.image = self.base_image
