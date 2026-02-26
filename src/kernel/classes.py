import pygame

class ContextMenu:
    def __init__(self, x, y, options, target_app):
        self.rect = pygame.Rect(x, y, 150, len(options) * 30 + 10)
        self.options, self.target = options, target_app
        self.font = pygame.font.SysFont("Segoe UI", 14)

    def draw(self, surface, mx, my):
        pygame.draw.rect(surface, (255, 255, 255), self.rect, border_radius=5)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 1, border_radius=5)
        for i, opt in enumerate(self.options):
            r = pygame.Rect(self.rect.x + 5, self.rect.y + 5 + (i * 30), 140, 25)
            if r.collidepoint(mx, my): pygame.draw.rect(surface, (230, 230, 230), r, border_radius=3)
            surface.blit(self.font.render(opt, True, (50, 50, 50)), (r.x + 10, r.y + 3))

    def get_choice(self, mx, my):
        if not self.rect.collidepoint(mx, my): return None
        idx = (my - (self.rect.y + 5)) // 30
        return self.options[int(idx)] if 0 <= idx < len(self.options) else None

class AppWindow:
    def __init__(self, name, app_module, icon):
        self.name, self.module, self.icon = name, app_module, icon
        self.app_data = self.module.init_data() if hasattr(self.module, "init_data") else {}
        
        # Default size check
        dw, dh = (self.module.config.get("width", 400), self.module.config.get("height", 300)) if hasattr(self.module, "config") else (400, 300)
        
        import random
        self.rect = pygame.Rect(100 + random.randint(0,100), 100 + random.randint(0,100), dw, dh)
        self.dragging = self.resizing = False
        self.offset_x = self.offset_y = 0

    def draw(self, surface, mx, my, is_active, close_img):
        pygame.draw.rect(surface, (255, 255, 255), self.rect, border_radius=8)
        pygame.draw.rect(surface, (180, 180, 180), self.rect, 2, border_radius=8)
        h_r = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, 30)
        pygame.draw.rect(surface, (230, 230, 230), h_r, border_top_left_radius=8, border_top_right_radius=8)
        
        if self.icon: surface.blit(pygame.transform.scale(self.icon, (18, 18)), (self.rect.x + 8, self.rect.y + 6))
        t = pygame.font.SysFont("Segoe UI", 12, bold=True).render(self.name.upper(), True, (50, 50, 50))
        surface.blit(t, (self.rect.x + 32, self.rect.y + 7))

        self.close_r = pygame.Rect(self.rect.right - 25, self.rect.y + 5, 20, 20)
        if close_img: surface.blit(close_img, (self.close_r.x, self.close_r.y))
        self.resize_r = pygame.Rect(self.rect.right - 15, self.rect.bottom - 15, 15, 15)
        
        # Content Clipping
        clip_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 30, self.rect.w - 4, self.rect.h - 32)
        surface.set_clip(clip_rect) 
        self.module.draw_content(surface, self.rect, self.app_data, is_active)
        surface.set_clip(None)
