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
            background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            background_img = None
    return platforms, enemies, items, goal, background_img, bg_file

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Merging Mario - Modular System")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 36)
    
    menu_font = pygame.font.SysFont("arial", 48, bold=True) 

    current_level = 1
    
    player = Player(50, SCREEN_HEIGHT - 150)
    platforms, enemies, items, goal, background_img, bg_file = load_level_data(current_level)
    
    camera_x = 0
    game_state = "MENU"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    

            game_state = handle_menu_events(event, game_state, SCREEN_WIDTH, SCREEN_HEIGHT)
            
            if event.type == pygame.KEYDOWN:
                if game_state != "MENU":
                    if event.key == pygame.K_r:
                        if game_state == "GAME_OVER":
                            player = Player(50, SCREEN_HEIGHT - 150)
                            platforms, enemies, items, goal, background_img, bg_file = load_level_data(current_level)
                            camera_x = 0
                            game_state = "PLAYING"
                        elif game_state == "LEVEL_COMPLETE":
                            current_level += 1
                            if current_level > 4: current_level = 1
                            player = Player(50, SCREEN_HEIGHT - 150)
                            platforms, enemies, items, goal, background_img, bg_file = load_level_data(current_level)
                            camera_x = 0
                            game_state = "PLAYING"

        if game_state == "PLAYING":
            keys = pygame.key.get_pressed()
            
            platforms.update() 
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

        
        if game_state == "MENU":
            draw_menu(screen, menu_font, font, SCREEN_WIDTH, SCREEN_HEIGHT, GREEN, WHITE, BLACK)
            
        else:
            if background_img:
                screen.blit(background_img, (0, 0))
            else:
                screen.fill(SKY_BLUE)

            for p in platforms: p.draw(screen, camera_x)
            for i in items: i.draw(screen, camera_x)
            for e in enemies: e.draw(screen, camera_x)
            goal.draw(screen, camera_x)
            
            if player.is_alive: 
                player.draw(screen, camera_x)

            if game_state == "GAME_OVER":
                text = font.render("DIED! Press 'R' to Restart", True, BRICK_RED)
                screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))
            elif game_state == "LEVEL_COMPLETE":
                text = font.render(f"LEVEL {current_level} DONE! Press 'R'", True, FLAG_GREEN)
                screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))

            info = font.render(f"Level: {current_level}", True, WHITE)
            screen.blit(info, (10, 10))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()