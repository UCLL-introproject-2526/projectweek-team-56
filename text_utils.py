import pygame

def render_text_with_outline(font, text, fg_color, outline_color=(0,0,0), outline_width=1):
    """Render `text` with a slim outline by blitting the outline color around the base text.

    Returns a Surface with per-pixel alpha.
    """
    base = font.render(text, True, fg_color)
    outline = font.render(text, True, outline_color)
    w, h = base.get_size()
    surf = pygame.Surface((w + 2 * outline_width, h + 2 * outline_width), pygame.SRCALPHA)

    # Blit outline at offsets around the center (skip center)
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx == 0 and dy == 0:
                continue
            surf.blit(outline, (dx + outline_width, dy + outline_width))

    # Blit main text centered inside the outline padding
    surf.blit(base, (outline_width, outline_width))
    return surf
