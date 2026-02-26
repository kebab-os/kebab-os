import pygame, sys, os, importlib.util, json
from datetime import datetime
from .classes import AppWindow, ContextMenu

def boot():
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except:
            pass
    
    pygame.init()
    
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

    try:
        pygame.scrap.init()
    except:
        print("Clipboard support not available")
    
    pygame.display.set_caption("kebabOS v3.0")

    ROOT = ".."; APPS_DIR = "applications"; DATA_FILE = "storage/data.json"
    
    def get_img(path, size, alpha=True):
        try:
            img = pygame.image.load(path)
            return pygame.transform.smoothscale(img.convert_alpha() if alpha else img.convert(), size)
        except: return None

    def save_data(pinned):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w") as f: json.dump({"pinned_apps": pinned}, f)

    # Load Assets
    pygame.mouse.set_visible(False)
    favicon = get_img('static/system/favicon.png', (16, 16))
    wallpaper = get_img('static/user/wallpaper.png', (WIDTH, HEIGHT), False)
    cursor_img = get_img('static/system/cursor.png', (15, 15))
    start_icon = get_img('static/system/start.png', (24, 24))
    close_icon = get_img('static/system/close.png', (20, 20))
    shutdown_icon = get_img('static/system/shutdown.png', (16, 16))

    if favicon:
        pygame.display.set_icon(favicon)

    apps_reg, open_wins, pinned_apps = {}, [], []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: pinned_apps = json.load(f).get("pinned_apps", [])

    for folder in os.listdir(APPS_DIR):
        p = f"{APPS_DIR}/{folder}"
        if os.path.isdir(p) and os.path.exists(f"{p}/app.py"):
            spec = importlib.util.spec_from_file_location("app", f"{p}/app.py")
            mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
            apps_reg[folder] = {'module': mod, 'icon': get_img(f"{p}/favicon.png", (22, 22))}

    font = pygame.font.SysFont("Segoe UI", 16); clock = pygame.time.Clock()
    start_open = False; active_menu = None

    while True:
        if wallpaper: screen.blit(wallpaper, (0,0))
        else: screen.fill((240, 240, 240))
        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

            # --- KEYBOARD ROUTING ---
            if event.type == pygame.KEYDOWN and open_wins:
                active_win = open_wins[-1]
                if hasattr(active_win.module, "handle_input"):
                    active_win.module.handle_input(event, active_win.app_data)

            # --- MOUSE & WINDOW LOGIC ---
            if active_menu and event.type == pygame.MOUSEBUTTONDOWN:
                choice = active_menu.get_choice(mx, my)
                target = active_menu.target
                if choice == "Open": open_wins.append(AppWindow(target, apps_reg[target]['module'], apps_reg[target]['icon']))
                elif choice == "Pin to Taskbar" and target not in pinned_apps: pinned_apps.append(target); save_data(pinned_apps)
                elif choice == "Unpin": pinned_apps.remove(target); save_data(pinned_apps)
                active_menu = None; continue

            clicked_ui = False
            for win in reversed(open_wins):
                if event.type == pygame.MOUSEBUTTONDOWN and win.rect.collidepoint(event.pos):
                    clicked_ui = True
                    if win.close_r.collidepoint(event.pos): open_wins.remove(win)
                    elif pygame.Rect(win.rect.right-15, win.rect.bottom-15, 15, 15).collidepoint(event.pos): win.resizing = True
                    else:
                        open_wins.remove(win); open_wins.append(win)
                        if pygame.Rect(win.rect.x, win.rect.y, win.rect.w, 30).collidepoint(event.pos):
                            win.dragging = True; win.offset_x, win.offset_y = win.rect.x - mx, win.rect.y - my
                    break
            
            if not clicked_ui and event.type == pygame.MOUSEBUTTONDOWN:
                if 4 <= mx <= 36 and HEIGHT - 36 <= my <= HEIGHT - 4: start_open = not start_open
                elif HEIGHT - 40 <= my <= HEIGHT:
                    for i, name in enumerate(pinned_apps):
                        if (45 + i*40) <= mx <= (77 + i*40):
                            if event.button == 1: open_wins.append(AppWindow(name, apps_reg[name]['module'], apps_reg[name]['icon']))
                            elif event.button == 3: active_menu = ContextMenu(mx, my, ["Unpin"], name)
                elif start_open:
                    items = list(apps_reg.keys()) + ["Shutdown"]; mh = len(items)*40+20; my_s = HEIGHT-45-mh
                    if 5 <= mx <= 205 and my_s <= my <= HEIGHT-45:
                        idx = int((my - (my_s + 10)) // 40)
                        if 0 <= idx < len(apps_reg):
                            n = list(apps_reg.keys())[idx]
                            if event.button == 1: open_wins.append(AppWindow(n, apps_reg[n]['module'], apps_reg[n]['icon'])); start_open = False
                            elif event.button == 3: active_menu = ContextMenu(mx, my, ["Open", "Pin to Taskbar"], n)
                        elif idx == len(apps_reg): pygame.quit(); sys.exit()
                    else: start_open = False

            if event.type == pygame.MOUSEBUTTONUP:
                for w in open_wins: w.dragging = w.resizing = False
            if event.type == pygame.MOUSEMOTION:
                for w in open_wins:
                    if w.dragging: w.rect.x, w.rect.y = mx + w.offset_x, my + w.offset_y
                    if w.resizing: w.rect.w, w.rect.h = max(300, mx-w.rect.x), max(200, my-w.rect.y)

        # Drawing
        for i, w in enumerate(open_wins): 
            is_act = (i == len(open_wins)-1)
            w.draw(screen, mx, my, is_act, close_icon)
            if is_act: pygame.draw.polygon(screen, (150, 150, 150), [(w.rect.right-2, w.rect.bottom-10), (w.rect.right-2, w.rect.bottom-2), (w.rect.right-10, w.rect.bottom-2)])
        
        pygame.draw.rect(screen, (240, 240, 240), (0, HEIGHT - 40, WIDTH, 40))
        s_r = pygame.Rect(4, HEIGHT - 36, 32, 32) # Uses HEIGHT
        if start_icon: screen.blit(start_icon, (8, HEIGHT - 32))
        
        run_names = [win.name for win in open_wins]
        for i, name in enumerate(pinned_apps):
            ix = 45 + i*40
            if name in apps_reg and apps_reg[name]['icon']: screen.blit(pygame.transform.scale(apps_reg[name]['icon'], (24, 24)), (ix, HEIGHT - 32))
            if name in run_names: pygame.draw.rect(screen, (0, 184, 148), (ix + 4, HEIGHT - 4, 16, 3), border_radius=2)

        if start_open:
            items = list(apps_reg.keys()) + ["Shutdown"]
            mh = len(items) * 40 + 20
            mr = pygame.Rect(5, HEIGHT - 45 - mh, 200, mh) 
            pygame.draw.rect(screen, (255, 255, 255), mr, border_radius=10)
            for i, item in enumerate(items):
                it_r = pygame.Rect(mr.x + 5, mr.y + 5 + (i * 40), 190, 35)
                if it_r.collidepoint(mx, my): pygame.draw.rect(screen, (240, 240, 240), it_r, border_radius=5)
                ic = apps_reg[item]['icon'] if item in apps_reg else shutdown_icon
                if ic: screen.blit(pygame.transform.scale(ic, (16, 16)), (it_r.x + 10, it_r.y + 10))
                screen.blit(font.render(item.capitalize(), True, (45, 52, 54)), (it_r.x + 35, it_r.y + 7))

        screen.blit(font.render(datetime.now().strftime("%H:%M:%S"), True, (45, 52, 54)), (WIDTH - 80, HEIGHT - 32))
        if active_menu: active_menu.draw(screen, mx, my)
        if cursor_img: screen.blit(cursor_img, (mx, my))
        pygame.display.flip(); clock.tick(60)
