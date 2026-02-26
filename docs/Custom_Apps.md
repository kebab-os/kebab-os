# Custom App Quick Start Guide

**To create a new app, create a folder in applications/ (e.g., applications/Notes) and add an app.py.**

---

## 1. The Essential Structure

Every app must have these components to talk to the kebabOS kernel:

```python
import pygame

# Define window defaults
config = {
    "width": 350,
    "height": 250
}

# This runs once when the app is opened
def init_data():
    return {"content": "Type here...", "color": (50, 50, 50)}

# This runs when your window is the active (top) one
def handle_input(event, data):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            data["content"] = data["content"][:-1]
        else:
            data["content"] += event.unicode

# This runs every frame
def draw_content(surface, rect, data, is_active):
    # Use 'rect' to stay inside your window boundaries
    font = pygame.font.SysFont("Arial", 16)
    text_surf = font.render(data["content"], True, data["color"])
    surface.blit(text_surf, (rect.x + 10, rect.y + 10))
```

## 2. Pro-Tips for Apps

1. Icons: Save a favicon.png in your app folder. The kernel finds it automatically.
2. Clipping: Don't worry about drawing over the taskbar; the Pygame Surface clipping in the kernel handles that for you.
3. Coordination: Always use rect.x and rect.y as your anchor points so your UI moves when the window is dragged.
