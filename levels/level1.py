import pygame
from settings import *
from sprites import Platform, Enemy, Item, Goal

def get_level_data():
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    items = pygame.sprite.Group()
    
    # Level 1: "The Ambush"
    platforms.add(Platform(0, SCREEN_HEIGHT - 40, 800, 40, GROUND_BROWN))
    platforms.add(Platform(900, SCREEN_HEIGHT - 40, 1000, 40, GROUND_BROWN))
    
    # Moving Platforms
    platforms.add(Platform(200, 450, 100, 20, move_x=100))
    platforms.add(Platform(500, 350, 100, 20, move_x=150))
    
    platforms.add(Platform(850, 300, 50, 20))
    platforms.add(Platform(1100, 400, 150, 20))
    platforms.add(Platform(1400, 300, 150, 20, move_x=100)) 
    
    enemies.add(Enemy(200, 530, 100))
    enemies.add(Enemy(500, 530, 150))
    enemies.add(Enemy(1100, 370, 120))
    enemies.add(Enemy(300, 200, 100)) # Flying
    
    items.add(Item(650, 220, "speed")) 
    goal = Goal(1800, SCREEN_HEIGHT - 40)
    
    return platforms, enemies, items, goal