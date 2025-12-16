import pygame
from settings import *
from sprites import Platform, Enemy, Item, Goal

def get_level_data():
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    items = pygame.sprite.Group()

    platforms.add(Platform(0, SCREEN_HEIGHT - 40, 2000, 40, GROUND_BROWN))
    platforms.add(Platform(500, 350, 50, 250)) 
    platforms.add(Platform(1200, 250, 50, 350))
    
    # Helper Moving Platform
    platforms.add(Platform(700, 200, 100, 20, move_x=300, speed=4))
    
    enemies.add(Enemy(600, 530, 100))
    enemies.add(Enemy(800, 530, 100))
    items.add(Item(400, 530, "jump"))
    goal = Goal(1900, SCREEN_HEIGHT - 40)

    return platforms, enemies, items, goal