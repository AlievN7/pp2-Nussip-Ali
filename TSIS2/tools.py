import pygame
from collections import deque


# Заливуа
def flood_fill(surface, pos, fill_color):
    x, y = int(pos[0]), int(pos[1])
    w, h = surface.get_size()

    #Если кликнули за пределами w, h выходим
    if not (0 <= x < w and 0 <= y < h):
        return

    # Целевой цвет, [:3] берёт только RGB без Alpha
    target_color = surface.get_at((x, y))[:3]
    fc = tuple(fill_color[:3])

    if target_color == fc:
        return

    surface.lock()
    try:
        #FIFO
        queue = deque()
        queue.append((x, y))
        visited = set()
        visited.add((x, y))

        while queue:
            cx, cy = queue.popleft()

            # Проверка цвет пикселя
            if surface.get_at((cx, cy))[:3] != target_color:
                continue

            surface.set_at((cx, cy), fill_color)

            # Добавляем соседей (4-связность)
            for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    finally:
        surface.unlock()


#Предпросмотр
def draw_shape_preview(screen, mode, start, end, color, brush_size, offset_y=0):
    sp = (start[0], start[1] + offset_y)
    ep = (end[0],   end[1]   + offset_y)

    if mode == 'line':
        pygame.draw.line(screen, color, sp, ep, brush_size)

    elif mode == 'rect':
        x = min(sp[0], ep[0])
        y = min(sp[1], ep[1])
        w = abs(ep[0] - sp[0])
        h = abs(ep[1] - sp[1])
        pygame.draw.rect(screen, color, (x, y, w, h), brush_size)

    elif mode == 'circle':
        dx = ep[0] - sp[0]
        dy = ep[1] - sp[1]
        r = int((dx**2 + dy**2) ** 0.5)
        if r > 0:
            pygame.draw.circle(screen, color, sp, r, brush_size)

    elif mode == 'square':
        side = min(abs(ep[0] - sp[0]), abs(ep[1] - sp[1]))
        x = min(sp[0], ep[0])
        y = min(sp[1], ep[1])
        pygame.draw.rect(screen, color, (x, y, side, side), brush_size)

    elif mode == 'rtriangle':
        pts = [sp, (sp[0], ep[1]), ep]
        pygame.draw.polygon(screen, color, pts, brush_size)

    elif mode == 'etriangle':
        mid_x = (sp[0] + ep[0]) // 2
        apex_y = sp[1] + int(abs(ep[0] - sp[0]) * 0.866)
        pts = [sp, ep, (mid_x, apex_y)]
        pygame.draw.polygon(screen, color, pts, brush_size)

    elif mode == 'rhombus':
        cx = (sp[0] + ep[0]) // 2
        cy = (sp[1] + ep[1]) // 2
        pts = [(cx, sp[1]), (ep[0], cy), (cx, ep[1]), (sp[0], cy)]
        pygame.draw.polygon(screen, color, pts, brush_size)


#Рисует фигуру
def commit_shape(canvas, mode, start, end, color, brush_size):

    sp = start
    ep = end

    if mode == 'line':
        pygame.draw.line(canvas, color, sp, ep, brush_size)

    elif mode == 'rect':
        x = min(sp[0], ep[0])
        y = min(sp[1], ep[1])
        w = abs(ep[0] - sp[0])
        h = abs(ep[1] - sp[1])
        pygame.draw.rect(canvas, color, (x, y, w, h), brush_size)

    elif mode == 'circle':
        dx = ep[0] - sp[0]
        dy = ep[1] - sp[1]
        r = int((dx**2 + dy**2) ** 0.5)
        if r > 0:
            pygame.draw.circle(canvas, color, sp, r, brush_size)

    elif mode == 'square':
        side = min(abs(ep[0] - sp[0]), abs(ep[1] - sp[1]))
        x = min(sp[0], ep[0])
        y = min(sp[1], ep[1])
        pygame.draw.rect(canvas, color, (x, y, side, side), brush_size)

    elif mode == 'rtriangle':
        pts = [sp, (sp[0], ep[1]), ep]
        pygame.draw.polygon(canvas, color, pts, brush_size)

    elif mode == 'etriangle':
        mid_x = (sp[0] + ep[0]) // 2
        apex_y = sp[1] + int(abs(ep[0] - sp[0]) * 0.866)
        pts = [sp, ep, (mid_x, apex_y)]
        pygame.draw.polygon(canvas, color, pts, brush_size)

    elif mode == 'rhombus':
        cx = (sp[0] + ep[0]) // 2
        cy = (sp[1] + ep[1]) // 2
        pts = [(cx, sp[1]), (ep[0], cy), (cx, ep[1]), (sp[0], cy)]
        pygame.draw.polygon(canvas, color, pts, brush_size)
