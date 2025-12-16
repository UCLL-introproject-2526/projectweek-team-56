import pygame
import sys

# --- New/Updated Color Definitions for Aesthetics ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DEEP_RED = (180, 0, 0)         # Primary background color
ACCENT_CYAN = (0, 190, 255)    # Button color
HOVER_CYAN = (0, 230, 255)     # Button hover color
BUTTON_BORDER_RED = (255, 80, 80) # Button border color (lighter red accent)


# --- Menu Drawing Function (Clean Red Aesthetic) ---
def draw_menu(screen, title_font, button_font, screen_width, screen_height, title_color, button_text_color, button_bg_color):
    """
    Draws the main game menu with a clean, high-contrast red aesthetic.
    
    Note: title_color, button_text_color, button_bg_color parameters 
    are kept for compatibility but the drawing now uses the hardcoded DEEP_RED/ACCENT_CYAN 
    for a controlled aesthetic.
    """
    
    # 1. Draw Solid Deep Red Background
    screen.fill(DEEP_RED)

    # 2. Draw Title with a Black Border (for maximum contrast against the red)
    
    # Render title text (WHITE)
    title_text = title_font.render("MERGING MARIO", True, WHITE) 
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))

    # Title Border/Shadow (BLACK)
    for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3)]:
        screen.blit(title_font.render("MERGING MARIO", True, BLACK), 
                    (title_rect.x + dx, title_rect.y + dy))

    # Actual Title (WHITE)
    screen.blit(title_text, title_rect)


    # 3. Define Button Properties (Adjusted for cleaner look)
    mouse_pos = pygame.mouse.get_pos()
    button_width = 320
    button_height = 70
    button_y_start = screen_height // 2 - button_height // 2 - 20
    button_spacing = 100 

    # --- Start Game Button ---
    start_button_rect = pygame.Rect(
        screen_width // 2 - button_width // 2,
        button_y_start,
        button_width,
        button_height
    )
    
    # Apply Hover Effect
    bg_color = HOVER_CYAN if start_button_rect.collidepoint(mouse_pos) else ACCENT_CYAN

    # Draw button background (Rounded Rect)
    pygame.draw.rect(screen, bg_color, start_button_rect, border_radius=15)
    
    # Draw button border (Lighter Red Accent)
    pygame.draw.rect(screen, BUTTON_BORDER_RED, start_button_rect, 5, border_radius=15)

    # Draw button text (BLACK for contrast on bright cyan)
    start_text = button_font.render("START GAME", True, BLACK)
    start_text_rect = start_text.get_rect(center=start_button_rect.center)
    screen.blit(start_text, start_text_rect)

    # --- Quit Button ---
    quit_button_rect = pygame.Rect(
        screen_width // 2 - button_width // 2,
        button_y_start + button_spacing,
        button_width,
        button_height
    )
    
    # Apply Hover Effect
    bg_color = HOVER_CYAN if quit_button_rect.collidepoint(mouse_pos) else ACCENT_CYAN

    # Draw button background (Rounded Rect)
    pygame.draw.rect(screen, bg_color, quit_button_rect, border_radius=15)
    
    # Draw button border (Lighter Red Accent)
    pygame.draw.rect(screen, BUTTON_BORDER_RED, quit_button_rect, 5, border_radius=15)
    
    # Draw button text (BLACK for contrast on bright cyan)
    quit_text = button_font.render("QUIT", True, BLACK)
    quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
    screen.blit(quit_text, quit_text_rect)
    
    return start_button_rect, quit_button_rect


# --- Menu Event Handling Function (No Change Needed) ---
def handle_menu_events(event, current_game_state, screen_width, screen_height):
    """
    Handles events (like mouse clicks) when the game is in the MENU state.
    NOTE: The button dimensions MUST match draw_menu()
    Returns the new game state.
    """
    if current_game_state == "MENU":
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Recalculate button positions using the passed arguments 
            button_width = 320 # Must match draw_menu
            button_height = 70 # Must match draw_menu
            button_y_start = screen_height // 2 - button_height // 2 - 20 # Must match draw_menu
            button_spacing = 100 # Must match draw_menu

            # Start Button Area
            start_button_rect = pygame.Rect(
                screen_width // 2 - button_width // 2,
                button_y_start,
                button_width,
                button_height
            )

            # Quit Button Area
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