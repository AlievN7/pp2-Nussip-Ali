import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    radius = 15
    mode = 'draw'        # текущий режим: draw, rect, circle, eraser
    points = []          # временный список точек текущей линии
    start_pos = None     # начальная позиция для rect и circle
    drawings = []        # список всех нарисованных фигур

    current_color = (0, 0, 255)
    colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,165,0)]

    WHITE = (255, 255, 255)

    # кнопки режимов: (название, режим, x позиция)
    buttons = [
        ("Draw",   'draw',   10),
        ("Rect",   'rect',   100),
        ("Circle", 'circle', 190),
        ("Eraser", 'eraser', 290),
    ]

    while True:
        pressed = pygame.key.get_pressed()
        alt_held  = pressed[pygame.K_LALT]  or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

            # Нажатие кнопки мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # проверяем нажали ли на кнопку режима
                    for (label, btn_mode, bx) in buttons:
                        btn_rect = pygame.Rect(bx, 445, 80, 30)
                        if btn_rect.collidepoint(event.pos):
                            mode = btn_mode
                            break
                    # проверяем нажали ли на кнопку цвета
                    for i, color in enumerate(colors):
                        color_rect = pygame.Rect(400 + i * 35, 445, 30, 30)
                        if color_rect.collidepoint(event.pos):
                            current_color = color
                            break
                    start_pos = event.pos
                    points = []
                elif event.button == 3:
                    radius = max(1, radius - 1)

            # Движение мыши
            if event.type == pygame.MOUSEMOTION:
                if mode == 'draw':
                    # сохраняем отрезок линии в drawings
                    points = points + [event.pos]
                    if len(points) >= 2:
                        drawings.append(('line', current_color, points[-2], points[-1], radius))
                elif mode == 'eraser':
                    # ластик — большой чёрный круг сохраняется в drawings
                    drawings.append(('eraser', (0,0,0), event.pos, radius * 2))

            # Отпускание кнопки мыши
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and start_pos:
                    if mode == 'rect':
                        x = min(start_pos[0], event.pos[0])
                        y = min(start_pos[1], event.pos[1])
                        w = abs(event.pos[0] - start_pos[0])
                        h = abs(event.pos[1] - start_pos[1])
                        drawings.append(('rect', current_color, (x, y, w, h)))
                    elif mode == 'circle':
                        dx = event.pos[0] - start_pos[0]
                        dy = event.pos[1] - start_pos[1]
                        r = int((dx**2 + dy**2) ** 0.5)
                        drawings.append(('circle', current_color, start_pos, r))
                    start_pos = None
                    points = []

        # Рисуем фон
        screen.fill((0, 0, 0))

        # Рисуем все сохранённые фигуры по порядку
        for drawing in drawings:
            if drawing[0] == 'line':
                drawLineBetween(screen, 0, drawing[2], drawing[3], drawing[4], drawing[1])
            elif drawing[0] == 'rect':
                pygame.draw.rect(screen, drawing[1], drawing[2], 2)
            elif drawing[0] == 'circle':
                pygame.draw.circle(screen, drawing[1], drawing[2], drawing[3], 2)
            elif drawing[0] == 'eraser':
                # ластик рисуется поверх всего
                pygame.draw.circle(screen, drawing[1], drawing[2], drawing[3])

        # Предпросмотр фигуры пока тянем мышь
        if start_pos and mode == 'rect':
            x = min(start_pos[0], mouse_pos[0])
            y = min(start_pos[1], mouse_pos[1])
            w = abs(mouse_pos[0] - start_pos[0])
            h = abs(mouse_pos[1] - start_pos[1])
            pygame.draw.rect(screen, current_color, (x, y, w, h), 1)
        elif start_pos and mode == 'circle':
            dx = mouse_pos[0] - start_pos[0]
            dy = mouse_pos[1] - start_pos[1]
            r = int((dx**2 + dy**2) ** 0.5)
            pygame.draw.circle(screen, current_color, start_pos, r, 1)

        # Панель UI внизу
        pygame.draw.rect(screen, (50, 50, 50), (0, 440, 640, 40))

        # Кнопки режимов
        for (label, btn_mode, bx) in buttons:
            color = (150, 150, 150) if mode == btn_mode else (100, 100, 100)
            pygame.draw.rect(screen, color, (bx, 445, 80, 30))
            txt = pygame.font.SysFont("Verdana", 12).render(label, True, (0,0,0))
            screen.blit(txt, (bx + 5, 452))

        # Кнопки выбора цвета
        for i, color in enumerate(colors):
            pygame.draw.rect(screen, color, (400 + i * 35, 445, 30, 30))
            if color == current_color:
                pygame.draw.rect(screen, WHITE, (400 + i * 35, 445, 30, 30), 2)

        pygame.display.flip()
        clock.tick(60)


def drawLineBetween(screen, index, start, end, width, current_color):
    # рисуем линию между двумя точками через кружки
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    if iterations == 0:
        return

    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, current_color, (x, y), width)

main()