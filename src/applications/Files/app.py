import pygame, os

config = {
    "width": 300,
    "height": 400
}

def init_data():
    return {}

def draw_content(screen, rect, data, is_active):
    inner = pygame.Rect(rect.x + 5, rect.y + 35, rect.w - 10, rect.h - 40)
    pygame.draw.rect(screen, (255, 255, 255), inner)
    f = pygame.font.SysFont("Segoe UI", 14)
    
    try: 
        files = os.listdir("storage/files")
    except: 
        files = []
    
    # Changed 'surface.blit' to 'screen.blit' to match the function argument
    screen.blit(f.render("Explorer:", True, (0, 184, 148)), (rect.x + 15, rect.y + 45))
    
    for i, file in enumerate(files):
        # Changed 'surface.blit' to 'screen.blit' here as well
        screen.blit(f.render(f"> {file}", True, (50, 50, 50)), (rect.x + 15, rect.y + 70 + (i * 22)))
