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

        self.current_platform = None

    def update(self, keys, platforms):
        dx = 0
        dy = 0

        current_speed = PLAYER_SPEED + self.speed_boost
        current_jump = JUMP_STRENGTH + self.jump_boost
        if keys[pygame.K_LEFT]:
            dx = -current_speed
        if keys[pygame.K_RIGHT]:
            dx = current_speed

        if self.on_ground and self.current_platform:
            if self.current_platform.move_dist > 0:
                dx += self.current_platform.speed * self.current_platform.direction

        if keys[pygame.K_SPACE] and self.on_ground:
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

    def merge_with_item(self, item_type):
        if item_type == "speed":
            self.speed_boost = 5
            self.image.fill(ITEM_BLUE)
        elif item_type == "jump":
            self.jump_boost = -5
            self.image.fill(ITEM_GOLD)

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))
