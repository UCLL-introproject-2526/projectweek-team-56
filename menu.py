import pygame
import sys
from text_utils import render_text_with_outline

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DEEP_RED = (180, 0, 0)        
ACCENT_CYAN = (0, 190, 255) 
HOVER_CYAN = (0, 230, 255) 
BUTTON_BORDER_COLOR = BLACK


def draw_menu(screen, title_font, button_font, screen_width, screen_height, title_color, button_text_color, button_bg_color):
    """
    Draws the main game menu with a clean, high-contrast red aesthetic 
    and strong BLACK button borders.
    """
    
    screen.fill(DEEP_RED)

    
    title_text = render_text_with_outline(title_font, "MERGING MARIO", title_color, BLACK, 1)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(title_text, title_rect)


    mouse_pos = pygame.mouse.get_pos()
    button_width = 320
    button_height = 70
    button_y_start = screen_height // 2 - button_height // 2 - 20
    button_spacing = 100 

    start_button_rect = pygame.Rect(
        screen_width // 2 - button_width // 2,
        button_y_start,
        button_width,
        button_height
    )
    
    bg_color = HOVER_CYAN if start_button_rect.collidepoint(mouse_pos) else ACCENT_CYAN

    pygame.draw.rect(screen, bg_color, start_button_rect, border_radius=15)
    
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, start_button_rect, 5, border_radius=15)

    start_text = render_text_with_outline(button_font, "START GAME", button_text_color, BLACK, 1)
    start_text_rect = start_text.get_rect(center=start_button_rect.center)
    screen.blit(start_text, start_text_rect)

    quit_button_rect = pygame.Rect(
        screen_width // 2 - button_width // 2,
        button_y_start + button_spacing,
        button_width,
        button_height
    )
    
    bg_color = HOVER_CYAN if quit_button_rect.collidepoint(mouse_pos) else ACCENT_CYAN

    pygame.draw.rect(screen, bg_color, quit_button_rect, border_radius=15)
    
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, quit_button_rect, 5, border_radius=15) 
    quit_text = render_text_with_outline(button_font, "QUIT", button_text_color, BLACK, 1)
    quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
    screen.blit(quit_text, quit_text_rect)
    
    return start_button_rect, quit_button_rect


def handle_menu_events(event, current_game_state, screen_width, screen_height):
    if current_game_state == "MENU":
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            button_width = 320 
            button_height = 70 
            button_y_start = screen_height // 2 - button_height // 2 - 20 
            button_spacing = 100 

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