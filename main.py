import pygame
import sys
from settings import *
from player import Player
from levels import create_level
from menu import draw_menu, handle_menu_events
from text_utils import render_text_with_outline


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

    level_width = SCREEN_WIDTH
    all_sprites = list(platforms) + list(enemies) + [goal]
    if all_sprites:

        max_x = max(s.rect.right for s in all_sprites if hasattr(s, 'rect'))
        level_width = max(level_width, max_x)

    return platforms, enemies, items, goal, background_img, bg_file, level_width


def main():
    pygame.init()
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("music/background.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        death_sfx = None
        jump_sfx = None
        goal_sfx = None
        coin_sfx = None
        try:
            death_sfx = pygame.mixer.Sound("music/death.wav")
        except Exception:
            try:
                death_sfx = pygame.mixer.Sound("assets/death.wav")
            except Exception:
                death_sfx = None
        try:
            jump_sfx = pygame.mixer.Sound("music/jump.wav")
        except Exception:
            try:
                jump_sfx = pygame.mixer.Sound("assets/jump.wav")
            except Exception:
                jump_sfx = None
        try:

            try:
                goal_sfx = pygame.mixer.Sound("music/goal.mp3")
            except Exception:
                try:
                    goal_sfx = pygame.mixer.Sound("music/goal.wav")
                except Exception:
                    try:
                        goal_sfx = pygame.mixer.Sound("assets/goal.mp3")
                    except Exception:
                        try:
                            goal_sfx = pygame.mixer.Sound("assets/goal.wav")
                        except Exception:
                            goal_sfx = None
        except Exception:
            goal_sfx = None
        try:

            for fname in ("music/coin.mp3", "music/coin.wav", "assets/coin.mp3", "assets/coin.wav"):
                try:
                    coin_sfx = pygame.mixer.Sound(fname)
                    break
                except Exception:
                    continue
        except Exception:
            coin_sfx = None
    except Exception:
        death_sfx = None
        pass
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Merging Mario - Modular System")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 36)

    menu_font = pygame.font.SysFont("arial", 48, bold=True)
    win_title_font = pygame.font.SysFont("arial", 72, bold=True)

    current_level = 1
    player = Player(50, SCREEN_HEIGHT - 150)
    death_count = 0
    need_coins_timer = 0
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

                            platforms, enemies, items, goal, background_img, bg_file, level_width = load_level_data(
                                current_level)
                            camera_x = 0
                            try:
                                pygame.mixer.music.unpause()
                            except Exception:
                                pass
                            game_state = "PLAYING"

                        elif game_state == "GAME_OVER":
                            player = Player(50, SCREEN_HEIGHT - 150)

                            platforms, enemies, items, goal, background_img, bg_file, level_width = load_level_data(
                                current_level)
                            camera_x = 0
                            try:
                                pygame.mixer.music.unpause()
                            except Exception:
                                pass
                            game_state = "PLAYING"

                        elif game_state == "LEVEL_COMPLETE":
                            if current_level >= 4:
                                game_state = "GAME_WIN"
                            else:
                                current_level += 1
                                player = Player(50, SCREEN_HEIGHT - 150)

                                platforms, enemies, items, goal, background_img, bg_file, level_width = load_level_data(
                                    current_level)
                                camera_x = 0
                                try:
                                    pygame.mixer.music.unpause()
                                except Exception:
                                    pass
                                game_state = "PLAYING"

                    elif event.key in (pygame.K_w, pygame.K_SPACE, pygame.K_UP):
                        try:
                            if jump_sfx and getattr(player, 'on_ground', False):
                                jump_sfx.play()
                        except Exception:
                            pass

                    elif event.key == pygame.K_q and game_state == "GAME_WIN":
                        running = False

        if game_state == "PLAYING":
            keys = pygame.key.get_pressed()

            platforms.update()
            player.update(keys, platforms)

            if player.rect.left < 0:
                player.rect.left = 0

            if player.rect.right > level_width:
                player.rect.right = level_width

            target_camera_x = player.rect.centerx - SCREEN_WIDTH // 2

            if target_camera_x < 0:
                target_camera_x = 0

            max_camera_x = level_width - SCREEN_WIDTH
            if max_camera_x < 0:
                max_camera_x = 0

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
                t = getattr(item, 'type', None)
                player.merge_with_item(t)

                try:
                    if t == 'coin' and coin_sfx:
                        coin_sfx.play()
                except Exception:
                    pass
                item.kill()

            if player.rect.colliderect(goal.rect):
                if getattr(player, 'gold', 0) >= 3:
                    if game_state != "LEVEL_COMPLETE":
                        try:
                            if goal_sfx:
                                goal_sfx.play()
                        except Exception:
                            pass
                    game_state = "LEVEL_COMPLETE"
                else:
                    need_coins_timer = 120

            if not player.is_alive:

                try:
                    if death_sfx:
                        death_sfx.play()
                except Exception:
                    pass

                # increment death counter
                try:
                    death_count += 1
                except Exception:
                    pass

                try:
                    pygame.mixer.music.pause()
                except Exception:
                    pass
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
                try:
                    text_surf = render_text_with_outline(
                        font, "DIED! Press 'R' to Restart", BRICK_RED, outline_color=BLACK, outline_width=1)
                    rect = text_surf.get_rect(
                        center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                    screen.blit(text_surf, rect)
                except Exception:
                    try:
                        text = font.render(
                            "DIED! Press 'R' to Restart", True, BRICK_RED)
                        screen.blit(text, (SCREEN_WIDTH//2 -
                                    text.get_width()//2, SCREEN_HEIGHT//2))
                    except Exception:
                        pass

            elif game_state == "LEVEL_COMPLETE":
                try:
                    text_surf = render_text_with_outline(
                        font, f"LEVEL {current_level} DONE! Press 'R'", FLAG_GREEN, outline_color=BLACK, outline_width=1)
                    rect = text_surf.get_rect(
                        center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                    screen.blit(text_surf, rect)
                except Exception:
                    try:
                        text = font.render(
                            f"LEVEL {current_level} DONE! Press 'R'", True, FLAG_GREEN)
                        screen.blit(text, (SCREEN_WIDTH//2 -
                                    text.get_width()//2, SCREEN_HEIGHT//2))
                    except Exception:
                        pass

            elif game_state == "GAME_WIN":
                overlay = pygame.Surface(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))

                try:
                    win_text_surf = render_text_with_outline(
                        win_title_font, "YOU WON!", ITEM_GOLD, outline_color=BLACK, outline_width=1)
                    screen.blit(win_text_surf, win_text_surf.get_rect(
                        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))
                except Exception:
                    try:
                        win_text = win_title_font.render(
                            "YOU WON!", True, ITEM_GOLD)
                        screen.blit(win_text, win_text.get_rect(
                            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))
                    except Exception:
                        pass

                try:
                    prompt_surf = render_text_with_outline(
                        font, "Press 'R' to Restart Game or 'Q' to Quit", WHITE, outline_color=BLACK, outline_width=1)
                    screen.blit(prompt_surf, prompt_surf.get_rect(
                        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
                except Exception:
                    try:
                        prompt_text = font.render(
                            "Press 'R' to Restart Game or 'Q' to Quit", True, WHITE)
                        screen.blit(prompt_text, prompt_text.get_rect(
                            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
                    except Exception:
                        pass

            try:
                info_surf = render_text_with_outline(
                    font, f"Level: {current_level}", WHITE, outline_color=BLACK, outline_width=1)
                screen.blit(info_surf, (10, 10))
            except Exception:
                try:
                    info = font.render(f"Level: {current_level}", True, WHITE)
                    screen.blit(info, (10, 10))
                except Exception:
                    pass

            try:
                gold_val = getattr(player, 'gold', 0)
                gold_surf = render_text_with_outline(
                    font, f"Gold: {gold_val}", ITEM_GOLD, outline_color=BLACK, outline_width=1)
                screen.blit(gold_surf, (10, 50))
            except Exception:
                try:
                    gold_text = font.render(
                        f"Gold: {getattr(player, 'gold', 0)}", True, ITEM_GOLD)
                    screen.blit(gold_text, (10, 50))
                except Exception:
                    pass

            try:
                death_surf = render_text_with_outline(
                    font, f"Deaths: {death_count}", WHITE, outline_color=BLACK, outline_width=1)
                screen.blit(death_surf, (10, 90))
            except Exception:
                try:
                    death_text = font.render(
                        f"Deaths: {death_count}", True, WHITE)
                    screen.blit(death_text, (10, 90))
                except Exception:
                    pass

            if need_coins_timer > 0:
                try:
                    msg = render_text_with_outline(font, "Need 3 coins to finish level!", BRICK_RED, outline_color=BLACK, outline_width=1)
                    screen.blit(msg, msg.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60)))
                except Exception:
                    try:
                        msg2 = font.render("Need 3 coins to finish level!", True, BRICK_RED)
                        screen.blit(msg2, (SCREEN_WIDTH//2 - msg2.get_width()//2, SCREEN_HEIGHT//2 - 60))
                    except Exception:
                        pass
                need_coins_timer -= 1

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
