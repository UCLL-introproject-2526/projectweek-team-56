import pygame
from settings import *
from sprites import Platform, Enemy, Item, Goal

def get_level_data():
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    items = pygame.sprite.Group()

    platforms.add(Platform(0, SCREEN_HEIGHT - 40, 3000, 40, GROUND_BROWN))
    for i in range(10):
        enemies.add(Enemy(400 + (i * 200), 530, 100))
        
    platforms.add(Platform(400, 350, 50, 20, move_x=100))
    platforms.add(Platform(800, 350, 50, 20, move_x=100))
    platforms.add(Platform(1200, 350, 50, 20, move_x=100))
    
    items.add(Item(200, 530, "speed"))
    goal = Goal(2800, SCREEN_HEIGHT - 40)

    return platforms, enemies, items, goal