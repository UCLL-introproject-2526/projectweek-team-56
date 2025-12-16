import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
DARK_GREY = (50, 50, 50)
LIGHT_GREY = (150, 150, 150)

def draw_menu(screen, title_font, button_font, screen_width, screen_height, title_color, button_text_color, button_bg_color):
    """
    Draws the main game menu to the screen.
    """
    screen.fill(DARK_GREY)

    title_text = title_font.render("MERGING MARIO", True, title_color)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(title_text, title_rect)

    button_width = 250
    button_height = 60
    button_y_start = screen_height // 2 - button_height // 2
    button_spacing = 80

    start_button_rect = pygame.Rect(
        screen_width // 2 - button_width // 2,
        button_y_start,
        button_width,
        button_height
    )
    
    pygame.draw.rect(screen, button_bg_color, start_button_rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, start_button_rect, 3, border_radius=10)

    start_text = button_font.render("START GAME", True, button_text_color)
    start_text_rect = start_text.get_rect(center=start_button_rect.center)
    screen.blit(start_text, start_text_rect)

    quit_button_rect = pygame.Rect(
        screen_width // 2 - button_width // 2,
        button_y_start + button_spacing,
        button_width,
        button_height
    )
    

    pygame.draw.rect(screen, button_bg_color, quit_button_rect, border_radius=10)

    pygame.draw.rect(screen, WHITE, quit_button_rect, 3, border_radius=10)
    
    quit_text = button_font.render("QUIT", True, button_text_color)
    quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
    screen.blit(quit_text, quit_text_rect)
    

    return start_button_rect, quit_button_rect


def handle_menu_events(event, current_game_state, screen_width, screen_height):
    """
    Handles events (like mouse clicks) when the game is in the MENU state.
    Requires screen dimensions (screen_width, screen_height) to calculate click areas.
    Returns the new game state.
    """
    if current_game_state == "MENU":
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            button_width = 250
            button_height = 60
            button_y_start = screen_height // 2 - button_height // 2
            button_spacing = 80

            start_button_rect = pygame.Rect(
                screen_width // 2 - button_width // 2,
                button_y_start,
                button_width,
                button_height
            )

            quit_button_rect = pygame.Rect(
                screen_width // 2 - button_width // 2,
                button_y_start + button_spacing,
                button_width,
                button_height
            )

            if start_button_rect.collidepoint(mouse_pos):
                return "PLAYING"
            elif quit_button_rect.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

    return current_game_state