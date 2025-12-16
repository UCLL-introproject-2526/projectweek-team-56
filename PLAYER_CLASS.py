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
        if keys[pygame.K_LEFT]:
            dx = -current_speed
        if keys[pygame.K_RIGHT]:
            dx = current_speed

        # 2. MOVING PLATFORM LOGIC (The "Stickiness")
        # If we are on a platform, add its speed to ours
        if self.on_ground and self.current_platform:
            if self.current_platform.move_dist > 0:  # Only if it's a moving one
                dx += self.current_platform.speed * self.current_platform.direction

        # 3. Jumping
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = current_jump
            self.on_ground = False
            self.current_platform = None  # Detach from platform when jumping

        # 4. Gravity
        self.velocity_y += GRAVITY
        dy += self.velocity_y

        # 5. X Collision
        self.rect.x += dx
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dx > 0:
                    self.rect.right = platform.rect.left
                elif dx < 0:
                    self.rect.left = platform.rect.right

        # 6. Y Collision
        self.rect.y += dy
        self.on_ground = False  # Reset every frame
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:  # Falling down
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.current_platform = platform  # REMEMBER THIS PLATFORM
                elif self.velocity_y < 0:  # Head bump
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
