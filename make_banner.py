import pygame

def create_special_banner():
    pygame.init()

    # GitHub için ideal boyut
    WIDTH, HEIGHT = 800, 320
    surface = pygame.Surface((WIDTH, HEIGHT))

    # --- RENKLER (Senin Kodundaki Temaya Uygun) ---
    SKY_BLUE = (100, 200, 255)
    GROUND_BROWN = (100, 50, 20)
    GRASS_GREEN = (50, 200, 50)
    
    # Player Renkleri (Kodundaki Logic'e göre)
    PLAYER_RED = (200, 50, 50)    # Normal
    PLAYER_BLUE = (0, 100, 255)   # Speed Boost
    PLAYER_GOLD = (255, 215, 0)   # Jump Boost
    
    PLATFORM_GRAY = (180, 180, 180)
    TEXT_WHITE = (255, 255, 255)
    SHADOW = (0, 0, 0)

    # 1. ARKA PLAN
    surface.fill(SKY_BLUE)

    # Bulutlar
    for pos in [(100, 80), (150, 60), (600, 100), (700, 80)]:
        pygame.draw.circle(surface, (255, 255, 255), pos, 30)
        pygame.draw.circle(surface, (255, 255, 255), (pos[0]+20, pos[1]), 30)

    # 2. ZEMİN (Altta)
    pygame.draw.rect(surface, GROUND_BROWN, (0, HEIGHT-60, WIDTH, 60))
    pygame.draw.rect(surface, GRASS_GREEN, (0, HEIGHT-60, WIDTH, 10))

    # 3. HAREKETLİ PLATFORM ÇİZİMİ (Kodundaki Logic'e Atıf)
    # Havada duran bir platform
    plat_rect = pygame.Rect(320, 200, 160, 20)
    pygame.draw.rect(surface, PLATFORM_GRAY, plat_rect)
    # Hareket ettiğini belli eden oklar (< >)
    font_arrow = pygame.font.SysFont("arial", 20, bold=True)
    arrow = font_arrow.render("<   MOVING   >", True, (50, 50, 50))
    surface.blit(arrow, (335, 198))

    # 4. KARAKTERLERİN ÇİZİMİ (Farklı Modlar)

    # A) Normal Player (Solda bekliyor)
    p_rect = pygame.Rect(50, HEIGHT-100, 30, 40)
    pygame.draw.rect(surface, PLAYER_RED, p_rect)
    # Göz
    pygame.draw.rect(surface, (255, 255, 255), (65, HEIGHT-95, 8, 8))
    # Etiket
    font_small = pygame.font.SysFont("arial", 14)
    lbl_norm = font_small.render("Normal", True, (255, 255, 255))
    surface.blit(lbl_norm, (45, HEIGHT-55))

    # B) SPEED Player (Mavi - Hızlı koşuyor efekti)
    p_speed_rect = pygame.Rect(200, HEIGHT-100, 30, 40)
    # Hız çizgileri (Arkasına)
    pygame.draw.line(surface, (255, 255, 255), (170, HEIGHT-90), (190, HEIGHT-90), 2)
    pygame.draw.line(surface, (255, 255, 255), (160, HEIGHT-80), (190, HEIGHT-80), 2)
    pygame.draw.rect(surface, PLAYER_BLUE, p_speed_rect)
    # Göz
    pygame.draw.rect(surface, (255, 255, 255), (215, HEIGHT-95, 8, 8))
    # Etiket
    lbl_spd = font_small.render("Speed Boost", True, PLAYER_BLUE)
    surface.blit(lbl_spd, (180, HEIGHT-55))

    # C) JUMP Player (Altın - Platformun üstünde zıplıyor)
    # Platformun biraz üstünde
    p_jump_rect = pygame.Rect(380, 140, 30, 40)
    pygame.draw.rect(surface, PLAYER_GOLD, p_jump_rect)
    # Göz
    pygame.draw.rect(surface, (255, 255, 255), (395, 145, 8, 8))
    # Parlama Efekti (Altın olduğu için)
    pygame.draw.circle(surface, (255, 255, 200), (380, 140), 5)
    # Etiket
    lbl_jmp = font_small.render("Jump Boost", True, (255, 200, 0))
    surface.blit(lbl_jmp, (360, 120))


    # 5. YAZILAR (Title)
    try:
        title_font = pygame.font.SysFont("arial black", 50)
        sub_font = pygame.font.SysFont("arial", 24, bold=True)
    except:
        title_font = pygame.font.SysFont(None, 60)
        sub_font = pygame.font.SysFont(None, 30)

    # Ana Başlık
    text_main = "SUPER PYGAME PRO"
    text_shadow = title_font.render(text_main, True, SHADOW)
    text_color = title_font.render(text_main, True, (255, 255, 255))
    
    # Başlığı Ortala (Sağ tarafa doğru)
    center_x = 620
    surface.blit(text_shadow, (center_x - text_shadow.get_width()//2 + 3, 53))
    surface.blit(text_color, (center_x - text_color.get_width()//2, 50))

    # Alt Başlık
    text_sub = sub_font.render("ADVANCED PHYSICS • TEAM 56", True, (50, 50, 50))
    surface.blit(text_sub, (center_x - text_sub.get_width()//2, 110))

    # Özellik Listesi (Hocaya show yapmak için)
    features = [
        "• Moving Platforms",
        "• Speed & Jump Items",
        "• Advanced Collision"
    ]
    
    start_y = 160
    for feat in features:
        f_surf = font_small.render(feat, True, (20, 20, 20))
        surface.blit(f_surf, (550, start_y))
        start_y += 20

    # 6. KAYDET
    pygame.image.save(surface, "banner_special.png")
    print("Özel banner oluşturuldu: 'banner_special.png'")
    pygame.quit()

if __name__ == "__main__":
    create_special_banner()