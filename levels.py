import pygame
from settings import *
from platforms import Platform
from enemy import Enemy, FlyingEnemy
from item import Item
from goal import Goal


def create_level(level_number):
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    items = pygame.sprite.Group()
    goal = None
    background = None

    if level_number == 1:
        platforms.add(Platform(0, SCREEN_HEIGHT - 40, 800, 40, GROUND_BROWN))
        platforms.add(Platform(900, SCREEN_HEIGHT -
                      40, 1000, 40, GROUND_BROWN))

        platforms.add(Platform(200, 450, 100, 20, move_x=100))
        platforms.add(Platform(500, 350, 100, 20, move_x=150))
        platforms.add(Platform(850, 300, 50, 20))
        platforms.add(Platform(1100, 400, 150, 20))
        platforms.add(Platform(1400, 300, 150, 20, move_x=100))

        enemies.add(Enemy(200, 530, 100))
        enemies.add(Enemy(500, 530, 150))
        enemies.add(Enemy(1100, 370, 120))
        enemies.add(Enemy(300, 200, 100))
        
        enemies.add(Enemy(950, 530, 140))
        
        enemies.add(FlyingEnemy(700, 260, 180, amplitude=26, osc_speed=0.09))
        enemies.add(FlyingEnemy(1300, 220, 160, amplitude=18, osc_speed=0.14))

        items.add(Item(650, 220, "speed"))
        
        items.add(Item(210, 420, "coin"))
        items.add(Item(500, 320, "coin"))
        items.add(Item(850, 270, "coin"))
        items.add(Item(1150, 370, "coin"))
        items.add(Item(1500, 260, "coin"))
        goal = Goal(1800, SCREEN_HEIGHT - 40)

    elif level_number == 2:
        platforms.add(Platform(0, SCREEN_HEIGHT - 40, 200, 40, GROUND_BROWN))
        platforms.add(Platform(250, 450, 150, 20, move_x=100, speed=2))

        enemies.add(Enemy(250, 420, 120))
        platforms.add(Platform(600, 350, 150, 20, move_x=200, speed=3))
        enemies.add(Enemy(600, 320, 120))
        
        enemies.add(Enemy(350, 530, 100))
        enemies.add(FlyingEnemy(900, 280, 220, amplitude=28, osc_speed=0.085))
        platforms.add(Platform(1000, 400, 500, 40, GROUND_BROWN))
        items.add(Item(325, 420, "jump"))
        
        items.add(Item(50, SCREEN_HEIGHT - 80, "coin"))
        items.add(Item(325, 380, "coin"))
        items.add(Item(600, 320, "coin"))
        items.add(Item(1200, 360, "coin"))
        goal = Goal(1400, 400)

    elif level_number == 3:
        platforms.add(Platform(0, SCREEN_HEIGHT - 40, 2000, 40, GROUND_BROWN))
        platforms.add(Platform(500, 350, 50, 250))
        platforms.add(Platform(1200, 250, 50, 350))
        platforms.add(Platform(700, 200, 100, 20, move_x=300, speed=4))
        enemies.add(Enemy(600, 530, 100))
        enemies.add(Enemy(800, 530, 100))
        
        enemies.add(Enemy(1000, 530, 120))
        enemies.add(Enemy(1400, 530, 140))
        enemies.add(FlyingEnemy(1400, 300, 280, amplitude=36, osc_speed=0.07))
        items.add(Item(400, 530, "jump"))
        items.add(Item(520, 320, "coin"))
        items.add(Item(700, 170, "coin"))
        items.add(Item(1200, 220, "coin"))
        items.add(Item(1600, 500, "coin"))
        goal = Goal(1900, SCREEN_HEIGHT - 40)

    elif level_number == 4:
        platforms.add(Platform(0, SCREEN_HEIGHT - 40, 2200, 40, GROUND_BROWN))
        platforms.add(Platform(2400, SCREEN_HEIGHT - 40, 800, 40, GROUND_BROWN))

        platforms.add(Platform(300, 440, 90, 18, move_x=160, speed=3))
        platforms.add(Platform(700, 380, 70, 18, move_x=220, speed=3))
        platforms.add(Platform(1100, 320, 60, 18, move_x=140, speed=3))
        platforms.add(Platform(1500, 260, 120, 18))
        platforms.add(Platform(1800, 320, 60, 18, move_x=200, speed=4))
        platforms.add(Platform(2100, 380, 80, 18))

        enemies.add(Enemy(420, 530, 110))
        enemies.add(Enemy(620, 530, 120))
        enemies.add(Enemy(820, 530, 140))
        enemies.add(Enemy(1000, 530, 150))
        enemies.add(Enemy(1300, 500, 160))
        enemies.add(Enemy(1700, 500, 170))
        enemies.add(FlyingEnemy(900, 200, 210, amplitude=40, osc_speed=0.06))
        enemies.add(FlyingEnemy(1400, 180, 240, amplitude=32, osc_speed=0.08))
        enemies.add(FlyingEnemy(2000, 240, 200, amplitude=28, osc_speed=0.09))

        items.add(Item(260, 410, "coin"))
        items.add(Item(420, 300, "coin"))
        items.add(Item(700, 340, "coin"))
        items.add(Item(1100, 280, "coin"))
        items.add(Item(1500, 220, "coin"))
        items.add(Item(2050, 360, "coin"))
        items.add(Item(2350, 500, "coin"))

        items.add(Item(380, 520, "speed"))
        goal = Goal(2800, SCREEN_HEIGHT - 40)

    try:
        background = LEVEL_BACKGROUNDS.get(level_number)
    except Exception:
        background = None

    for enemy in list(enemies):
        
        if isinstance(enemy, FlyingEnemy):
            continue

        start_x = getattr(enemy, 'start_x', enemy.rect.x)
        platform_under = None
        min_top = None
        for p in platforms:
            if not hasattr(p, 'rect'):
                continue
            if p.rect.left <= start_x <= p.rect.right:
                if min_top is None or p.rect.top < min_top:
                    platform_under = p
                    min_top = p.rect.top

        if platform_under:
            enemy.rect.y = platform_under.rect.top - enemy.rect.height
        else:
            
            enemy.rect.y = SCREEN_HEIGHT - 40 - enemy.rect.height

    return platforms, enemies, items, goal, background
