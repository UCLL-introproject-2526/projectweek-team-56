import pygame
from text_utils import render_text_with_outline

def create_special_banner():
    pygame.init()

    WIDTH, HEIGHT = 800, 320
    surface = pygame.Surface((WIDTH, HEIGHT))

    SKY_BLUE = (100, 200, 255)
    GROUND_BROWN = (100, 50, 20)
    GRASS_GREEN = (50, 200, 50)
    
    PLAYER_RED = (200, 50, 50)    
    PLAYER_BLUE = (0, 100, 255)   
    PLAYER_GOLD = (255, 215, 0)   
    
    PLATFORM_GRAY = (180, 180, 180)
    TEXT_WHITE = (255, 255, 255)
    SHADOW = (0, 0, 0)

    surface.fill(SKY_BLUE)

    for pos in [(100, 80), (150, 60), (600, 100), (700, 80)]:
        pygame.draw.circle(surface, (255, 255, 255), pos, 30)
        pygame.draw.circle(surface, (255, 255, 255), (pos[0]+20, pos[1]), 30)

    pygame.draw.rect(surface, GROUND_BROWN, (0, HEIGHT-60, WIDTH, 60))
    pygame.draw.rect(surface, GRASS_GREEN, (0, HEIGHT-60, WIDTH, 10))

    plat_rect = pygame.Rect(320, 200, 160, 20)
    pygame.draw.rect(surface, PLATFORM_GRAY, plat_rect)
    font_arrow = pygame.font.SysFont("arial", 20, bold=True)
    arrow = render_text_with_outline(font_arrow, "<   MOVING   >", (50, 50, 50), (0,0,0), 1)
    surface.blit(arrow, (335, 198))


    p_rect = pygame.Rect(50, HEIGHT-100, 30, 40)
    pygame.draw.rect(surface, PLAYER_RED, p_rect)
    pygame.draw.rect(surface, (255, 255, 255), (65, HEIGHT-95, 8, 8))
    font_small = pygame.font.SysFont("arial", 14)
    lbl_norm = render_text_with_outline(font_small, "Normal", (255, 255, 255), (0,0,0), 1)
    surface.blit(lbl_norm, (45, HEIGHT-55))

    p_speed_rect = pygame.Rect(200, HEIGHT-100, 30, 40)
    pygame.draw.line(surface, (255, 255, 255), (170, HEIGHT-90), (190, HEIGHT-90), 2)
    pygame.draw.line(surface, (255, 255, 255), (160, HEIGHT-80), (190, HEIGHT-80), 2)
    pygame.draw.rect(surface, PLAYER_BLUE, p_speed_rect)
    pygame.draw.rect(surface, (255, 255, 255), (215, HEIGHT-95, 8, 8))
    lbl_spd = render_text_with_outline(font_small, "Speed Boost", PLAYER_BLUE, (0,0,0), 1)
    surface.blit(lbl_spd, (180, HEIGHT-55))

    p_jump_rect = pygame.Rect(380, 140, 30, 40)
    pygame.draw.rect(surface, PLAYER_GOLD, p_jump_rect)
    pygame.draw.rect(surface, (255, 255, 255), (395, 145, 8, 8))
    pygame.draw.circle(surface, (255, 255, 200), (380, 140), 5)
    lbl_jmp = render_text_with_outline(font_small, "Jump Boost", (255, 200, 0), (0,0,0), 1)
    surface.blit(lbl_jmp, (360, 120))


    try:
        title_font = pygame.font.SysFont("arial black", 50)
        sub_font = pygame.font.SysFont("arial", 24, bold=True)
    except:
        title_font = pygame.font.SysFont(None, 60)
        sub_font = pygame.font.SysFont(None, 30)

    text_main = "SUPER PYGAME PRO"
    text_color = render_text_with_outline(title_font, text_main, (255,255,255), (0,0,0), 1)
    
    center_x = 620
    surface.blit(text_color, (center_x - text_color.get_width()//2, 50))

    text_sub = render_text_with_outline(sub_font, "ADVANCED PHYSICS • TEAM 56", (50, 50, 50), (0,0,0), 1)
    surface.blit(text_sub, (center_x - text_sub.get_width()//2, 110))

    features = [
        "• Moving Platforms",
        "• Speed & Jump Items",
        "• Advanced Collision"
    ]
    
    start_y = 160
    for feat in features:
        f_surf = render_text_with_outline(font_small, feat, (20, 20, 20), (0,0,0), 1)
        surface.blit(f_surf, (550, start_y))
        start_y += 20

    pygame.image.save(surface, "banner_special.png")
    print("Özel banner oluşturuldu: 'banner_special.png'")
    pygame.quit()

if __name__ == "__main__":
    create_special_banner()