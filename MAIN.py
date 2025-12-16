import pygame
import sys

# --- SETTINGS & CONSTANTS ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Physics
GRAVITY = 0.8
JUMP_STRENGTH = -16
PLAYER_SPEED = 5
ENEMY_SPEED = 3

# Colors
SKY_BLUE = (135, 206, 235)
BRICK_RED = (200, 50, 50)   # Mario Color
GROUND_BROWN = (100, 50, 20)
PLATFORM_GRAY = (150, 150, 150)
MOVING_PLATFORM_COLOR = (100, 100, 180)
ENEMY_PURPLE = (128, 0, 128)
FLAG_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
ITEM_BLUE = (0, 0, 255)
ITEM_GOLD = (255, 215, 0)

# --- CLASSES ---

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(BRICK_RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
        self.on_ground = False
        self.is_alive = True
        self.speed_boost = 0
        self.jump_boost = 0
        
        # NEW: Remember which platform we are standing on
        self.current_platform = None

    def update(self, keys, platforms):
        dx = 0
        dy = 0
        
        current_speed = PLAYER_SPEED + self.speed_boost
        current_jump = JUMP_STRENGTH + self.jump_boost

        # 1. Input Movement
        if keys[pygame.K_LEFT]: dx = -current_speed
        if keys[pygame.K_RIGHT]: dx = current_speed
        
        # 2. MOVING PLATFORM LOGIC (The "Stickiness")
        # If we are on a platform, add its speed to ours
        if self.on_ground and self.current_platform:
            if self.current_platform.move_dist > 0: # Only if it's a moving one
                dx += self.current_platform.speed * self.current_platform.direction

        # 3. Jumping
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = current_jump
            self.on_ground = False
            self.current_platform = None # Detach from platform when jumping

        # 4. Gravity
        self.velocity_y += GRAVITY
        dy += self.velocity_y

        # 5. X Collision
        self.rect.x += dx
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dx > 0: self.rect.right = platform.rect.left
                elif dx < 0: self.rect.left = platform.rect.right

        # 6. Y Collision
        self.rect.y += dy
        self.on_ground = False # Reset every frame
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0: # Falling down
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.current_platform = platform # REMEMBER THIS PLATFORM
                elif self.velocity_y < 0: # Head bump
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

        if self.rect.y > SCREEN_HEIGHT + 100:
            self.is_alive = False

    def merge_with_item(self, item_type):
        if item_type == "speed":
            self.speed_boost = 5
            self.image.fill(ITEM_BLUE)
        elif item_type == "jump":
            self.jump_boost = -5
            self.image.fill(ITEM_GOLD)

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=PLATFORM_GRAY, move_x=0, speed=2):
        super().__init__()
        self.image = pygame.Surface((width, height))
        
        if move_x > 0:
            self.image.fill(MOVING_PLATFORM_COLOR)
        else:
            self.image.fill(color)
            
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.start_x = x
        self.move_dist = move_x
        self.speed = speed
        self.direction = 1

    def update(self):
        if self.move_dist > 0:
            self.rect.x += self.speed * self.direction
            
            if self.rect.x > self.start_x + self.move_dist:
                self.direction = -1
            elif self.rect.x < self.start_x:
                self.direction = 1

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, distance):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(ENEMY_PURPLE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x = x
        self.distance = distance
        self.direction = 1 

    def update(self):
        self.rect.x += self.direction * ENEMY_SPEED
        if self.rect.x > self.start_x + self.distance:
            self.direction = -1
        elif self.rect.x < self.start_x:
            self.direction = 1

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((20, 20))
        if self.type == "speed": self.image.fill(ITEM_BLUE)
        elif self.type == "jump": self.image.fill(ITEM_GOLD)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(FLAG_GREEN)
        self.rect = self.image.get_rect(bottomleft=(x, y))

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))

# --- LEVEL DESIGN ---
def create_level(level_number):
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    items = pygame.sprite.Group()
    goal = None
    
    if level_number == 1:
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
        enemies.add(Enemy(300, 200, 100))
        
        items.add(Item(650, 220, "speed")) 
        goal = Goal(1800, SCREEN_HEIGHT - 40)
        
    elif level_number == 2:
        platforms.add(Platform(0, SCREEN_HEIGHT - 40, 200, 40, GROUND_BROWN))
        
        # Moving platforms train!
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
        
        # Helper Moving Platform
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

    return platforms, enemies, items, goal

# --- MAIN GAME ---

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Merging Mario - Sticky Platforms")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 36)

    current_level = 1
    player = Player(50, SCREEN_HEIGHT - 150)
    platforms, enemies, items, goal = create_level(current_level)
    
    camera_x = 0
    game_state = "PLAYING"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if game_state == "GAME_OVER":
                        player = Player(50, SCREEN_HEIGHT - 150)
                        platforms, enemies, items, goal = create_level(current_level)
                        camera_x = 0
                        game_state = "PLAYING"
                    elif game_state == "LEVEL_COMPLETE":
                        current_level += 1
                        if current_level > 4: current_level = 1
                        player = Player(50, SCREEN_HEIGHT - 150)
                        platforms, enemies, items, goal = create_level(current_level)
                        camera_x = 0
                        game_state = "PLAYING"

        if game_state == "PLAYING":
            keys = pygame.key.get_pressed()
            
            # Update Platforms FIRST so player knows where they are
            platforms.update() 
            
            # Update Player (Includes Sticky Logic)
            player.update(keys, platforms)

            target_camera_x = player.rect.centerx - SCREEN_WIDTH // 2
            if target_camera_x < 0: target_camera_x = 0
            camera_x += (target_camera_x - camera_x) * 0.1

            for enemy in enemies:
                enemy.update()

            hit_list = pygame.sprite.spritecollide(player, enemies, False)
            for enemy in hit_list:
                if player.velocity_y > 0 and player.rect.bottom < enemy.rect.centery + 15:
                    enemy.kill()
                    player.velocity_y = -12 
                else:
                    player.is_alive = False

            hit_items = pygame.sprite.spritecollide(player, items, True)
            for item in hit_items:
                player.merge_with_item(item.type)
                item.kill()

            if player.rect.colliderect(goal.rect):
                game_state = "LEVEL_COMPLETE"

            if not player.is_alive:
                game_state = "GAME_OVER"

        screen.fill(SKY_BLUE)
        for p in platforms: p.draw(screen, camera_x)
        for i in items: i.draw(screen, camera_x)
        for e in enemies: e.draw(screen, camera_x)
        goal.draw(screen, camera_x)
        if player.is_alive: player.draw(screen, camera_x)

        if game_state == "GAME_OVER":
            text = font.render("DIED! Press 'R' to Restart", True, BRICK_RED)
            screen.blit(text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))
        elif game_state == "LEVEL_COMPLETE":
            text = font.render(f"LEVEL {current_level} DONE! Press 'R'", True, FLAG_GREEN)
            screen.blit(text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))

        info = font.render(f"Level: {current_level}", True, WHITE)
        screen.blit(info, (10, 10))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()