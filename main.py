import pygame
import sys
from settings import *
from player import Player
from levels import create_level
from menu import draw_menu, handle_menu_events


def load_level_data(level_num):
    platforms, enemies, items, goal, bg_file = create_level(level_num)
    background_img = None
    if bg_file:
        try:
            background_img = pygame.image.load(bg_file).convert()
            background_img = pygame.transform.scale(
                background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            background_img = None
            
    # Calculate Level Width: Find the rightmost edge of all platforms and the goal
    level_width = SCREEN_WIDTH # Default minimum width
    all_sprites = list(platforms) + list(enemies) + [goal]
    if all_sprites:
        # Find the maximum x-coordinate (right edge)
        max_x = max(s.rect.right for s in all_sprites if hasattr(s, 'rect'))
        level_width = max(level_width, max_x)

    # Note: We now return level_width
    return platforms, enemies, items, goal, background_img, bg_file, level_width


def main():
    pygame.init()
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("music/background.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except Exception:
        pass
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Merging Mario - Modular System")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 36)

    menu_font = pygame.font.SysFont("arial", 48, bold=True)
    win_title_font = pygame.font.SysFont("arial", 72, bold=True)

    current_level = 1

    # Receive level_width from load_level_data
    player = Player(50, SCREEN_HEIGHT - 150)
    platforms, enemies, items, goal, background_img, bg_file, level_width = load_level_data(
        current_level)

    camera_x = 0
    game_state = "MENU"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            game_state = handle_menu_events(
                event, game_state, SCREEN_WIDTH, SCREEN_HEIGHT)

            if event.type == pygame.KEYDOWN:
                if game_state != "MENU":
                    if event.key == pygame.K_r:
                        if game_state == "GAME_WIN":
                            current_level = 1
                            player = Player(50, SCREEN_HEIGHT - 150)
                            # Re-receive level_width
                            platforms, enemies, items, goal, background_img, bg_file, level_width = load_level_data(
                                current_level)
                            camera_x = 0
                            game_state = "PLAYING"

                        elif game_state == "GAME_OVER":
                            player = Player(50, SCREEN_HEIGHT - 150)
                            # Re-receive level_width
                            platforms, enemies, items, goal, background_img, bg_file, level_width = load_level_data(
                                current_level)
                            camera_x = 0
                            game_state = "PLAYING"

                        elif game_state == "LEVEL_COMPLETE":
                            if current_level >= 4:
                                game_state = "GAME_WIN"
                            else:
                                current_level += 1
                                player = Player(50, SCREEN_HEIGHT - 150)
                                # Re-receive level_width
                                platforms, enemies, items, goal, background_img, bg_file, level_width = load_level_data(
                                    current_level)
                                camera_x = 0
                                game_state = "PLAYING"
                    elif event.key == pygame.K_q and game_state == "GAME_WIN":
                        running = False

        if game_state == "PLAYING":
            keys = pygame.key.get_pressed()

            platforms.update()
            player.update(keys, platforms)
            
            # --- NEW: World Boundary Check (Clamping Player Position) ---
            # 1. Left Boundary (World X = 0)
            if player.rect.left < 0:
                player.rect.left = 0
                
            # 2. Right Boundary (World X = level_width)
            if player.rect.right > level_width:
                player.rect.right = level_width


            # --- Camera Logic Updated to respect Level Width ---
            target_camera_x = player.rect.centerx - SCREEN_WIDTH // 2
            
            # Clamp target_camera_x to prevent showing areas left of the start (0)
            if target_camera_x < 0:
                target_camera_x = 0
            
            # Clamp the camera to the maximum possible right position
            max_camera_x = level_width - SCREEN_WIDTH
            if max_camera_x < 0: max_camera_x = 0 # If level is smaller than screen
            
            if target_camera_x > max_camera_x:
                target_camera_x = max_camera_x
                
            camera_x += (target_camera_x - camera_x) * 0.1

            for enemy in enemies:
                enemy.update()

            hit_list = pygame.sprite.spritecollide(player, enemies, False)
            for enemy in hit_list:
                if getattr(enemy, 'death_started', False):
                    continue
                if player.velocity_y > 0 and player.rect.bottom < enemy.rect.centery + 15:
                    if hasattr(enemy, 'start_death'):
                        enemy.start_death()
                    else:
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

        if game_state == "MENU":
            draw_menu(screen, menu_font, font, SCREEN_WIDTH,
                      SCREEN_HEIGHT, GREEN, WHITE, BLACK)

        else:
            if background_img:
                screen.blit(background_img, (0, 0))
            else:
                screen.fill(SKY_BLUE)

            for p in platforms:
                p.draw(screen, camera_x)
            for i in items:
                i.draw(screen, camera_x)
            for e in enemies:
                e.draw(screen, camera_x)
            goal.draw(screen, camera_x)

            if player.is_alive and game_state != "GAME_WIN":
                player.draw(screen, camera_x)

            if game_state == "GAME_OVER":
                text = font.render(
                    "DIED! Press 'R' to Restart", True, BRICK_RED)
                screen.blit(text, (SCREEN_WIDTH//2 -
                                   text.get_width()//2, SCREEN_HEIGHT//2))

            elif game_state == "LEVEL_COMPLETE":
                text = font.render(
                    f"LEVEL {current_level} DONE! Press 'R'", True, FLAG_GREEN)
                screen.blit(text, (SCREEN_WIDTH//2 -
                                   text.get_width()//2, SCREEN_HEIGHT//2))

            elif game_state == "GAME_WIN":
                overlay = pygame.Surface(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))

                win_text = win_title_font.render("YOU WON!", True, ITEM_GOLD)
                screen.blit(win_text, win_text.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))

                prompt_text = font.render(
                    "Press 'R' to Restart Game or 'Q' to Quit", True, WHITE)
                screen.blit(prompt_text, prompt_text.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

            info = font.render(f"Level: {current_level}", True, WHITE)
            screen.blit(info, (10, 10))

            try:
                gold_text = font.render(
                    f"Gold: {player.gold}", True, ITEM_GOLD)
            except Exception:
                gold_text = font.render("Gold: 0", True, ITEM_GOLD)
            screen.blit(gold_text, (10, 50))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass
    sys.exit()


if __name__ == "__main__":
    main()
