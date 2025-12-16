import pygame
from settings import *
from sprites import Platform, Enemy, Item, Goal

def get_level_data():
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    items = pygame.sprite.Group()

    platforms.add(Platform(0, SCREEN_HEIGHT - 40, 200, 40, GROUND_BROWN))
    
    platforms.add(Platform(250, 450, 150, 20, move_x=100, speed=2))
    enemies.add(Enemy(250, 420, 120))
    
    platforms.add(Platform(600, 350, 150, 20, move_x=200, speed=3))
    enemies.add(Enemy(600, 320, 120))
    
    platforms.add(Platform(1000, 400, 500, 40, GROUND_BROWN))
    items.add(Item(325, 420, "jump"))
    goal = Goal(1400, 400)

    return platforms, enemies, items, goal