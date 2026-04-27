import sys
import pygame
from datetime import datetime
from tools import flood_fill, draw_shape_preview, commit_shape


WIN_W,  WIN_H    = 1000, 600
#верхняя панель
TOP_H            = 44
#нижняя панель    
BOT_H            = 56        
CANVAS_Y         = TOP_H
CANVAS_H         = WIN_H - TOP_H - BOT_H   # 500 px
TOOLBAR_Y        = WIN_H - BOT_H

BRUSH_SIZES = {1: 2, 2: 5, 3: 10}

PALETTE = [
    (0,   0,   0),    # черный
    (128, 128, 128),  # серый
    (255,  0,   0),   # красный
    (200, 80,   0),   # оранжевый
    (200, 200,  0),   # желтый
    (0,  180,   0),   # зеленый
    (0,    0, 255),   # синий
    (120,  0, 200),   # фиолетовый
    (0,  180, 200),   # сине-зеленый
    (255, 255, 255),  # белый
]

TOOLS = [
    ("Pencil",   "pencil"),
    ("Line",     "line"),
    ("Rect",     "rect"),
    ("Circle",   "circle"),
    ("Eraser",   "eraser"),
    ("Square",   "square"),
    ("R-Tri",    "rtriangle"),
    ("E-Tri",    "etriangle"),
    ("Rhombus",  "rhombus"),
    ("Fill",     "fill"),
    ("Text",     "text"),
]

SHAPE_MODES = {"line", "rect", "circle", "square", "rtriangle", "etriangle", "rhombus"}


#Перевод экранной кординаты в коорлинаты холста, отнимаем у верхней панели
def screen_to_canvas(pos):
    return (pos[0], pos[1] - CANVAS_Y)

#Перевод координаты холста в кординаты экрана, плюсуем у верхней панели
def canvas_to_screen(pos):
    """Координаты холста → экранные."""
    return (pos[0], pos[1] + CANVAS_Y)

#Проверка находится ли точка в области холста
def in_canvas(pos):
    return 0 <= pos[0] < WIN_W and CANVAS_Y <= pos[1] < CANVAS_Y + CANVAS_H


#главный цикл 
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Paint — Extended  |  Ctrl+S сохранить  |  1/2/3 размер кисти")
    clock = pygame.time.Clock()

    #Холст
    canvas = pygame.Surface((WIN_W, CANVAS_H))
    canvas.fill((255, 255, 255))

    #Шрифты
    font_btn   = pygame.font.SysFont("Verdana", 11, bold=True)
    font_text  = pygame.font.SysFont("Verdana", 20)
    font_small = pygame.font.SysFont("Verdana", 12)
    font_tip   = pygame.font.SysFont("Verdana", 10)

    # Состояние
    mode          = "pencil"
    current_color = (0, 0, 0)
    brush_key     = 2           #размер кисти 1,2,3
    start_pos     = None        #начальные координаты холста
    save_msg      = ""          #всплывающее уведомление о сохранении
    save_timer    = 0

    #Текстовый инструмент
    text_pos   = None   #начальные координаты холста
    text_buf   = ""

    #Ширина кнопки инструмента
    n = len(TOOLS)
    BTN_W = WIN_W // n

    #Основной цикл
    running = True
    while running:
        dt = clock.tick(60)
        brush_size = BRUSH_SIZES[brush_key]
        mouse_scr  = pygame.mouse.get_pos()
        mouse_cnv  = screen_to_canvas(mouse_scr)
        pressed    = pygame.key.get_pressed()
        ctrl       = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        alt        = pressed[pygame.K_LALT]  or pressed[pygame.K_RALT]

        #Таймер уведомления о сохранении
        if save_timer > 0:
            save_timer -= dt

        #Обработка событий
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            #Клавиатура
            elif event.type == pygame.KEYDOWN:

                #Выход
                if (event.key == pygame.K_w and ctrl) or (event.key == pygame.K_F4 and alt):
                    running = False

                #Переключение размера кисти 1,2,3)
                elif event.key == pygame.K_1:
                    brush_key = 1
                elif event.key == pygame.K_2:
                    brush_key = 2
                elif event.key == pygame.K_3:
                    brush_key = 3

                #Ctrl+S сохранение
                elif event.key == pygame.K_s and ctrl:
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    name = f"canvas_{ts}.png"
                    pygame.image.save(canvas, name)
                    save_msg   = f"Сохранено: {name}"
                    save_timer = 3000  # 3 секунды

                #Ввод текста
                elif mode == "text" and text_pos is not None:
                    if event.key == pygame.K_RETURN:
                        if text_buf.strip():
                            surf = font_text.render(text_buf, True, current_color)
                            canvas.blit(surf, text_pos)
                        text_pos = None
                        text_buf = ""
                    elif event.key == pygame.K_ESCAPE:
                        text_pos = None
                        text_buf = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_buf = text_buf[:-1]
                    elif event.unicode and event.unicode.isprintable():
                        text_buf += event.unicode

                #Esc вне текстового режима, обнуляет позицию и набранный текст
                elif event.key == pygame.K_ESCAPE:
                    text_pos = None
                    text_buf = ""

            #Нажатие кнопки мыши
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked_ui = False

                #Палитра цветов верхняя панель
                for i, c in enumerate(PALETTE):
                    r = pygame.Rect(6 + i * 38, 7, 32, 30)
                    if r.collidepoint(event.pos):
                        current_color = c
                        clicked_ui    = True
                        break

                #Кнопки размера кисти верхняя панель, справа
                if not clicked_ui:
                    for sk in (1, 2, 3):
                        rx = WIN_W - 155 + (sk - 1) * 50
                        r  = pygame.Rect(rx, 7, 44, 30)
                        if r.collidepoint(event.pos):
                            brush_key  = sk
                            clicked_ui = True
                            break

                #Кнопки инструментов нижняя панель
                if not clicked_ui:
                    for i, (label, btn_mode) in enumerate(TOOLS):
                        r = pygame.Rect(i * BTN_W + 1, TOOLBAR_Y + 8, BTN_W - 2, BOT_H - 16)
                        if r.collidepoint(event.pos):
                            mode       = btn_mode
                            start_pos  = None
                            text_pos   = None
                            text_buf   = ""
                            clicked_ui = True
                            break

                #Действие на холсте
                if not clicked_ui and in_canvas(event.pos):
                    cp = screen_to_canvas(event.pos)
                    if mode == "fill":
                        flood_fill(canvas, cp, current_color)
                    elif mode == "text":
                        text_pos = cp
                        text_buf = ""
                    else:
                        start_pos = cp
                        #Точка при клике
                        if mode == "pencil":
                            r = max(1, brush_size // 2)
                            pygame.draw.circle(canvas, current_color, cp, r)
                        elif mode == "eraser":
                            pygame.draw.circle(canvas, (255, 255, 255), cp, brush_size * 3)

            #Движение мыши
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0] and in_canvas(event.pos) and start_pos:
                    cp = screen_to_canvas(event.pos)
                    if mode == "pencil":
                        pygame.draw.line(canvas, current_color, start_pos, cp, brush_size)
                        start_pos = cp
                    elif mode == "eraser":
                        pygame.draw.line(canvas, (255, 255, 255), start_pos, cp, brush_size * 5)
                        start_pos = cp

            #Отпускание кнопки мыши
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if start_pos and in_canvas(event.pos) and mode in SHAPE_MODES:
                    cp = screen_to_canvas(event.pos)
                    commit_shape(canvas, mode, start_pos, cp, current_color, brush_size)
                start_pos = None

        #Отрисовка
        screen.fill((30, 30, 30))

        #Холст
        screen.blit(canvas, (0, CANVAS_Y))

        #Live-preview фигуры при перетаскивании
        if start_pos and mode in SHAPE_MODES:
            draw_shape_preview(screen, mode, start_pos, mouse_cnv, current_color, brush_size, offset_y=CANVAS_Y)

        #Круг вокруг ластика
        if mode == "eraser":
            pygame.draw.circle(screen, (180, 180, 180), mouse_scr, brush_size * 3, 1)

        #Превью ввода текста
        if mode == "text" and text_pos is not None:
            cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
            preview = font_text.render(text_buf + cursor, True, current_color)
            screen.blit(preview, canvas_to_screen(text_pos))
        elif mode == "text" and text_pos is None:
            #Если выбран режим текст но клика не было, подсказка
            hint = font_tip.render("Кликните на холст чтобы начать ввод текста", True, (180, 180, 180))
            screen.blit(hint, (5, CANVAS_Y + CANVAS_H - 20))

        #Верхняя панель
        pygame.draw.rect(screen, (45, 45, 45), (0, 0, WIN_W, TOP_H))

        #Палитра
        for i, c in enumerate(PALETTE):
            rx, ry = 6 + i * 38, 7
            pygame.draw.rect(screen, c, (rx, ry, 32, 30))
            #Рамка выбранного цвета
            if c == current_color:
                pygame.draw.rect(screen, (255, 255, 255), (rx, ry, 32, 30), 3)
            else:
                pygame.draw.rect(screen, (80, 80, 80), (rx, ry, 32, 30), 1)

        #Метка Размер
        lbl = font_small.render("Размер:", True, (200, 200, 200))
        screen.blit(lbl, (WIN_W - 200, 14))

        #Кнопки размера
        size_names = {1: "S", 2: "M", 3: "B"}
        size_px    = {1: "2px", 2: "5px", 3: "10px"}
        for sk in (1, 2, 3):
            rx   = WIN_W - 155 + (sk - 1) * 50
            active = (sk == brush_key)
            bg   = (220, 200, 60) if active else (80, 80, 80)
            pygame.draw.rect(screen, bg, (rx, 7, 44, 30), border_radius=4)
            name_surf = font_btn.render(f"{size_names[sk]}", True, (0, 0, 0) if active else (200, 200, 200))
            px_surf   = font_tip.render(size_px[sk], True, (50, 50, 50) if active else (150, 150, 150))
            screen.blit(name_surf, (rx + 5, 9))
            screen.blit(px_surf,   (rx + 5, 23))

        #Нижняя панель
        pygame.draw.rect(screen, (45, 45, 45), (0, TOOLBAR_Y, WIN_W, BOT_H))

        for i, (label, btn_mode) in enumerate(TOOLS):
            bx     = i * BTN_W + 1
            active = (mode == btn_mode)
            bg     = (140, 140, 160) if active else (75, 75, 80)
            pygame.draw.rect(screen, bg, (bx, TOOLBAR_Y + 8, BTN_W - 2, BOT_H - 16), border_radius=4)
            txt = font_btn.render(label, True, (0, 0, 0) if active else (210, 210, 210))
            tw  = txt.get_width()
            screen.blit(txt, (bx + (BTN_W - 2 - tw) // 2, TOOLBAR_Y + 19))

        #Разделители между кнопками инструментов
        for i in range(1, n):
            x = i * BTN_W
            pygame.draw.line(screen, (30, 30, 30), (x, TOOLBAR_Y + 8), (x, WIN_H - 8))

        #Уведомление о сохранении
        if save_timer > 0:
            alpha = min(255, save_timer // 4)
            s = font_small.render(save_msg, True, (80, 255, 80))
            s.set_alpha(alpha)
            screen.blit(s, (10, TOOLBAR_Y - 22))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
