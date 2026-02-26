import pygame

config = {"width": 500, "height": 400}

def init_data():
    return {"buffer": ""}

def handle_input(event, data):
    if event.key == pygame.K_BACKSPACE: data["buffer"] = data["buffer"][:-1]
    elif event.key == pygame.K_RETURN: data["buffer"] += "\n"
    elif event.unicode.isprintable(): data["buffer"] += event.unicode

def draw_content(surface, rect, data, is_active):
    inner = pygame.Rect(rect.x + 5, rect.y + 35, rect.w - 10, rect.h - 40)
    pygame.draw.rect(surface, (252, 252, 252), inner)
    f = pygame.font.SysFont("Consolas", 14)
    lines = data["buffer"].split("\n")
    for i, line in enumerate(lines):
        ly = rect.y + 40 + (i * 18)
        ts = f.render(line, True, (30, 30, 30))
        surface.blit(ts, (rect.x + 10, ly))
        if is_active and i == len(lines)-1 and (pygame.time.get_ticks()//500)%2==0:
            pygame.draw.line(surface, (30,30,30), (rect.x+10+ts.get_width(), ly), (rect.x+10+ts.get_width(), ly+14), 2)
