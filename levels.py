import pygame
from settings import *
# Yeni importlar:
from platforms import Platform
from enemy import Enemy
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
        platforms.add(Platform(900, SCREEN_HEIGHT - 40, 1000, 40, GROUND_BROWN))
        
        platforms.add(Platform(200, 450, 100, 20, move_x=100))
        platforms.add(Platform(500, 350, 100, 20, move_x=150))
        platforms.add(Platform(850, 300, 50, 20))
        platforms.add(Platform(1100, 400, 150, 20))
        platforms.add(Platform(1400, 300, 150, 20, move_x=100)) 
        
        enemies.add(Enemy(200, 530, 100))
        enemies.add(Enemy(500, 530, 150))
        enemies.add(Enemy(1100, 370, 120))
        enemies.add(Enemy(300, 200, 100))
        
        items.add(Item(650, 220, "speed")) 
        goal = Goal(1800, SCREEN_HEIGHT - 40)
        
    elif level_number == 2:
        platforms.add(Platform(0, SCREEN_HEIGHT - 40, 200, 40, GROUND_BROWN))
        platforms.add(Platform(250, 450, 150, 20, move_x=100, speed=2))
        enemies.add(Enemy(250, 420, 120))
        platforms.add(Platform(600, 350, 150, 20, move_x=200, speed=3))
        enemies.add(Enemy(600, 320, 120))
        platforms.add(Platform(1000, 400, 500, 40, GROUND_BROWN))
        items.add(Item(325, 420, "jump"))
        goal = Goal(1400, 400)

    elif level_number == 3:
        platforms.add(Platform(0, SCREEN_HEIGHT - 40, 2000, 40, GROUND_BROWN))
        platforms.add(Platform(500, 350, 50, 250)) 
        platforms.add(Platform(1200, 250, 50, 350))
        platforms.add(Platform(700, 200, 100, 20, move_x=300, speed=4))
        enemies.add(Enemy(600, 530, 100))
        enemies.add(Enemy(800, 530, 100))
        items.add(Item(400, 530, "jump"))
        goal = Goal(1900, SCREEN_HEIGHT - 40)

    elif level_number == 4:
        platforms.add(Platform(0, SCREEN_HEIGHT - 40, 3000, 40, GROUND_BROWN))
        for i in range(10):
            enemies.add(Enemy(400 + (i * 200), 530, 100))
        platforms.add(Platform(400, 350, 50, 20, move_x=100))
        platforms.add(Platform(800, 350, 50, 20, move_x=100))
        platforms.add(Platform(1200, 350, 50, 20, move_x=100))
        items.add(Item(200, 530, "speed"))
        goal = Goal(2800, SCREEN_HEIGHT - 40)

    # pick a background image filename for this level (optional)
    try:
        background = LEVEL_BACKGROUNDS.get(level_number)
    except Exception:
        background = None

    return platforms, enemies, items, goal, background