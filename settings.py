import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

GRAVITY = 0.8
JUMP_STRENGTH = -16
PLAYER_SPEED = 5
ENEMY_SPEED = 3

# Global kill counter (shared across modules)
KILL_COUNT = 0


SKY_BLUE = (135, 206, 235)
BRICK_RED = (200, 50, 50)
GROUND_BROWN = (100, 50, 20)
PLATFORM_GRAY = (150, 150, 150)
MOVING_PLATFORM_COLOR = (100, 100, 180)
ENEMY_PURPLE = (128, 0, 128)
FLAG_GREEN = (0, 255, 0) 
WHITE = (255, 255, 255)


BLACK = (0, 0, 0)
GREEN = (0, 180, 0) 

ITEM_BLUE = (0, 0, 255)
ITEM_GOLD = (255, 215, 0)


BACKGROUND_IMAGE = "assets/coolbg.jpg"
LEVEL_BACKGROUNDS = {
    1: "assets/bg1.jpg",
    2: "assets/bg2.jpg",
    3: "assets/bg3.jpg",
    4: "assets/bg4.jpg",
    5: "assets/bg5.jpg",
}