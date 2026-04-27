import pygame
import sys
import random
import json
import time
from db import create_tables, save_session, get_top10, get_personal_best

pygame.init()
pygame.mixer.init()

# Размеры
W, H = 600, 480
SEG = 20

# Цвета
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
GRAY   = (50, 50, 50)
DARK   = (30, 30, 30)
POISON_COLOR = (120, 0, 0)
OBSTACLE_COLOR = (80, 80, 80)
GOLD   = (255, 215, 0)
BLUE   = (0, 100, 255)
ORANGE = (255, 140, 0)
PURPLE = (160, 0, 200)

# Шрифты
font_big   = pygame.font.SysFont("Verdana", 48)
font_med   = pygame.font.SysFont("Verdana", 28)
font_small = pygame.font.SysFont("Verdana", 18)

display = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

#Настройки
def load_settings():
    try:
        with open("settings.json") as f:
            return json.load(f)
    except:
        return {"snake_color": [0, 255, 0], "grid": False, "sound": True}

def save_settings(s):
    with open("settings.json", "w") as f:
        json.dump(s, f, indent=4)

settings = load_settings()

#Инициализация базы данных
create_tables()

# Рисование кнопок
def draw_button(text, x, y, w, h, color=(80, 80, 80), text_color=WHITE):
    pygame.draw.rect(display, color, (x, y, w, h), border_radius=6)
    t = font_small.render(text, True, text_color)
    display.blit(t, (x + (w - t.get_width()) // 2, y + (h - t.get_height()) // 2))

def btn_hit(x, y, w, h, pos):
    return pygame.Rect(x, y, w, h).collidepoint(pos)

def spawn_pos(snake, obstacles=None):
    obstacles = obstacles or []
    while True:
        fx = random.randint(0, W // SEG - 1) * SEG
        fy = random.randint(0, H // SEG - 1) * SEG
        if (fx, fy) not in snake and (fx, fy) not in obstacles:
            return fx, fy

def draw_grid():
    for x in range(0, W, SEG):
        pygame.draw.line(display, (40, 40, 40), (x, 0), (x, H))
    for y in range(0, H, SEG):
        pygame.draw.line(display, (40, 40, 40), (0, y), (W, y))

#Экраны
def screen_username():
    username = ""
    while True:
        display.fill(DARK)
        t = font_med.render("Enter your username:", True, WHITE)
        display.blit(t, (W // 2 - t.get_width() // 2, 150))
        pygame.draw.rect(display, WHITE, (150, 210, 300, 40), 2)
        u = font_med.render(username, True, WHITE)
        display.blit(u, (160, 215))
        draw_button("Confirm", W // 2 - 60, 280, 120, 40)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username:
                    return username
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_hit(W // 2 - 60, 280, 120, 40, event.pos) and username:
                    return username

def screen_menu(username):
    while True:
        display.fill(DARK)
        t = font_big.render("SNAKE", True, WHITE)
        display.blit(t, (W // 2 - t.get_width() // 2, 60))
        u = font_small.render(f"Player: {username}", True, GRAY)
        display.blit(u, (10, 10))

        draw_button("Play",        W//2-80, 160, 160, 45)
        draw_button("Leaderboard", W//2-80, 220, 160, 45)
        draw_button("Settings",    W//2-80, 280, 160, 45)
        draw_button("Quit",        W//2-80, 340, 160, 45)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                p = event.pos
                if btn_hit(W//2-80, 160, 160, 45, p): return "play"
                if btn_hit(W//2-80, 220, 160, 45, p): return "leaderboard"
                if btn_hit(W//2-80, 280, 160, 45, p): return "settings"
                if btn_hit(W//2-80, 340, 160, 45, p):
                    pygame.quit(); sys.exit()

def screen_leaderboard():
    rows = get_top10()
    while True:
        display.fill(DARK)
        t = font_med.render("TOP 10", True, WHITE)
        display.blit(t, (W // 2 - t.get_width() // 2, 20))

        headers = font_small.render("Rank  Username            Score  Level  Date", True, GRAY)
        display.blit(headers, (20, 60))
        pygame.draw.line(display, GRAY, (20, 80), (W - 20, 80))

        for i, (uname, score, level, played_at) in enumerate(rows):
            date_str = played_at.strftime("%Y-%m-%d") if played_at else ""
            line = f"{i+1:<5} name: {uname:<15} score: {score:<7} level: {level:<6} {date_str}"
            color = GOLD if i == 0 else WHITE
            txt = font_small.render(line, True, color)
            display.blit(txt, (20, 90 + i * 30))

        draw_button("Back", 20, H - 55, 100, 40)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_hit(20, H - 55, 100, 40, event.pos):
                    return

def screen_settings():
    global settings
    color_options = [[0,255,0],[0,0,255],[255,255,0],[255,165,0],[255,0,255]]
    color_names   = ["Green","Blue","Yellow","Orange","Magenta"]
    color_idx = 0
    for i, c in enumerate(color_options):
        if c == settings["snake_color"]:
            color_idx = i

    while True:
        display.fill(DARK)
        t = font_med.render("Settings", True, WHITE)
        display.blit(t, (W // 2 - t.get_width() // 2, 30))

        sound_txt = "Sound: ON" if settings["sound"] else "Sound: OFF"
        grid_txt  = "Grid: ON"  if settings["grid"]  else "Grid: OFF"
        color_txt = f"Snake color: {color_names[color_idx]}"

        draw_button(sound_txt, W//2-100, 120, 200, 45)
        draw_button(grid_txt,  W//2-100, 180, 200, 45)
        draw_button(color_txt, W//2-100, 240, 200, 45)

        # предпросмотр цвета
        pygame.draw.rect(display, color_options[color_idx], (W//2+115, 240, 45, 45), border_radius=4)

        draw_button("Save & Back", W//2-70, 320, 140, 45, color=(30,130,30))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                p = event.pos
                if btn_hit(W//2-100, 120, 200, 45, p):
                    settings["sound"] = not settings["sound"]
                if btn_hit(W//2-100, 180, 200, 45, p):
                    settings["grid"] = not settings["grid"]
                if btn_hit(W//2-100, 240, 200, 45, p):
                    color_idx = (color_idx + 1) % len(color_options)
                    settings["snake_color"] = color_options[color_idx]
                if btn_hit(W//2-70, 320, 140, 45, p):
                    save_settings(settings)
                    return

def screen_gameover(score, level, personal_best):
    while True:
        display.fill((60, 0, 0))
        t = font_big.render("GAME OVER", True, RED)
        display.blit(t, (W//2 - t.get_width()//2, 80))

        lines = [
            f"Score: {score}",
            f"Level: {level}",
            f"Personal best: {personal_best}",
        ]
        for i, line in enumerate(lines):
            txt = font_med.render(line, True, WHITE)
            display.blit(txt, (W//2 - txt.get_width()//2, 180 + i * 45))

        draw_button("Retry",     W//2-130, 360, 120, 45, color=(30,130,30))
        draw_button("Main Menu", W//2+10,  360, 120, 45)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_hit(W//2-130, 360, 120, 45, event.pos): return "retry"
                if btn_hit(W//2+10,  360, 120, 45, event.pos): return "menu"

#Игровой цикл
def generate_obstacles(snake, level, existing=None):
    existing = existing or []
    count = (level - 2) * 3  # 3 блока за каждый уровень начиная с 3
    count = min(count, 20)
    obstacles = []
    attempts = 0
    while len(obstacles) < count and attempts < 1000:
        attempts += 1
        ox = random.randint(0, W // SEG - 1) * SEG
        oy = random.randint(0, H // SEG - 1) * SEG
        pos = (ox, oy)
        # не ставим рядом со змейкой (буфер 2 сегмента)
        too_close = any(abs(ox - sx) <= SEG*2 and abs(oy - sy) <= SEG*2 for sx, sy in snake)
        if pos not in snake and pos not in obstacles and not too_close:
            obstacles.append(pos)
    return obstacles

def run_game(username):
    global settings
    SNAKE_COLOR = tuple(settings["snake_color"])
    personal_best = get_personal_best(username)

    # Состояние змейки
    snake     = [(W//2, H//2), (W//2 - SEG, H//2), (W//2 - SEG*2, H//2)]
    direction = "RIGHT"
    next_dir  = "RIGHT"
    speed     = 7
    score     = 0
    level     = 1
    obstacles = []

    # Еда
    food1 = spawn_pos(snake)
    food2 = spawn_pos(snake)
    food2_timer = pygame.time.get_ticks()  # food2 исчезает через 5 сек

    # Яд
    poison = None
    poison_timer = 0

    # Пауэрап
    powerup      = None
    powerup_type = None
    powerup_spawn_time = 0
    POWERUP_FIELD_DURATION = 8000  # ms на поле

    # Активный эффект пауэрапа
    active_effect      = None
    active_effect_start = 0
    EFFECT_DURATION    = 5000  # ms

    # Щит
    shield = False

    food_count = 0  # счётчик съеденной еды для уровня

    def spawn_powerup():
        nonlocal powerup, powerup_type, powerup_spawn_time
        if powerup is None:
            powerup_type = random.choice(["speed", "slow", "shield"])
            powerup = spawn_pos(snake, obstacles)
            powerup_spawn_time = pygame.time.get_ticks()

    # Спавним первый пауэрап через 10 сек
    next_powerup_spawn = pygame.time.get_ticks() + 10000

    running = True
    while running:
        now = pygame.time.get_ticks()
        dt  = clock.tick(speed)

        # События
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP)    and direction != "DOWN":  next_dir = "UP"
                if event.key in (pygame.K_s, pygame.K_DOWN)  and direction != "UP":    next_dir = "DOWN"
                if event.key in (pygame.K_a, pygame.K_LEFT)  and direction != "RIGHT": next_dir = "LEFT"
                if event.key in (pygame.K_d, pygame.K_RIGHT) and direction != "LEFT":  next_dir = "RIGHT"

        direction = next_dir

        # Движение
        hx, hy = snake[0]
        if direction == "UP":    hy -= SEG
        if direction == "DOWN":  hy += SEG
        if direction == "LEFT":  hx -= SEG
        if direction == "RIGHT": hx += SEG
        new_head = (hx, hy)

        # Столкновения 
        hit_wall = hx < 0 or hx >= W or hy < 0 or hy >= H
        hit_self = new_head in snake
        hit_obs  = new_head in obstacles

        if (hit_wall or hit_self or hit_obs):
            if shield:
                shield = False
                # телепорт на безопасную позицию
                new_head = spawn_pos(snake, obstacles)
                hx, hy = new_head
            else:
                save_session(username, score, level)
                pb = get_personal_best(username)
                return screen_gameover(score, level, pb)

        snake.insert(0, new_head)

        # Еда 1
        ate = False
        if new_head == food1:
            score += 1
            food_count += 1
            food1 = spawn_pos(snake, obstacles)
            ate = True

        # Еда 2 (исчезает через 5 сек) 
        if new_head == food2:
            score += 5
            food_count += 1
            food2 = spawn_pos(snake, obstacles)
            food2_timer = now
            ate = True
        elif now - food2_timer > 5000:
            food2 = spawn_pos(snake, obstacles)
            food2_timer = now

        # Яд 
        if poison and new_head == poison:
            # укорачиваем на 2
            snake = snake[:-2] if len(snake) > 3 else snake[:1]
            if len(snake) <= 1:
                save_session(username, score, level)
                pb = get_personal_best(username)
                return screen_gameover(score, level, pb)
            poison = None
            ate = True

        if not ate:
            snake.pop()

        # Уровень
        if food_count > 0 and food_count % 3 == 0:
            new_level = food_count // 3 + 1
            if new_level > level:
                level = new_level
                speed = min(7 + level, 20)
                if level >= 3:
                    obstacles = generate_obstacles(snake, level)
                food_count = food_count  # не сбрасываем

        # Яд (спавн раз в 15 сек)
        if poison is None and now % 15000 < dt + 100:
            poison = spawn_pos(snake, obstacles)

        # Пауэрап 
        if now >= next_powerup_spawn and powerup is None:
            spawn_powerup()

        if powerup and now - powerup_spawn_time > POWERUP_FIELD_DURATION:
            powerup = None
            powerup_type = None
            next_powerup_spawn = now + 15000

        if powerup and new_head == powerup:
            if powerup_type == "shield":
                shield = True
            else:
                active_effect = powerup_type
                active_effect_start = now
            powerup = None
            powerup_type = None
            next_powerup_spawn = now + 15000

        # Эффект
        if active_effect and now - active_effect_start > EFFECT_DURATION:
            if active_effect == "speed": speed = min(7 + level, 20)
            if active_effect == "slow":  speed = min(7 + level, 20)
            active_effect = None

        if active_effect == "speed": speed = min(7 + level + 5, 25)
        if active_effect == "slow":  speed = max(3, 7 + level - 4)

        # Отрисовка
        display.fill(BLACK)
        if settings["grid"]:
            draw_grid()

        # Препятствия
        for obs in obstacles:
            pygame.draw.rect(display, WHITE, (*obs, SEG, SEG))

        # Змейка
        for i, seg in enumerate(snake):
            color = SNAKE_COLOR if i > 0 else tuple(min(255, c+60) for c in SNAKE_COLOR)
            pygame.draw.rect(display, color, (*seg, SEG, SEG), border_radius=3)

        # Щит — обводка вокруг головы
        if shield:
            pygame.draw.rect(display, BLUE, (*snake[0], SEG, SEG), 2, border_radius=3)

        # Еда
        pygame.draw.rect(display, GREEN, (*food1, SEG, SEG), border_radius=4)
        pygame.draw.rect(display, GOLD,  (*food2, SEG, SEG), border_radius=4)

        # Яд
        if poison:
            pygame.draw.rect(display, POISON_COLOR, (*poison, SEG, SEG), border_radius=4)

        # Пауэрап
        if powerup:
            pu_color = {"speed": ORANGE, "slow": BLUE, "shield": PURPLE}.get(powerup_type, WHITE)
            pygame.draw.rect(display, pu_color, (*powerup, SEG, SEG), border_radius=4)
            label = font_small.render(powerup_type[0].upper(), True, WHITE)
            display.blit(label, (powerup[0]+3, powerup[1]+2))

        # HUD
        hud_lines = [
            f"Score: {score}   Level: {level}",
            f"Best: {personal_best}",
        ]
        for i, line in enumerate(hud_lines):
            txt = font_small.render(line, True, WHITE)
            display.blit(txt, (8, 8 + i * 22))

        # Активный эффект
        if active_effect:
            remaining = max(0, (EFFECT_DURATION - (now - active_effect_start)) // 1000)
            eff_txt = font_small.render(f"{active_effect.upper()} {remaining}s", True, ORANGE)
            display.blit(eff_txt, (W - eff_txt.get_width() - 8, 8))

        if shield:
            sh_txt = font_small.render("SHIELD", True, BLUE)
            display.blit(sh_txt, (W - sh_txt.get_width() - 8, 30))

        pygame.display.update()

# Главный цикл
def main():
    username = screen_username()
    while True:
        choice = screen_menu(username)
        if choice == "play":
            result = run_game(username)
            if result == "menu":
                continue
            elif result == "retry":
                result2 = run_game(username)
        elif choice == "leaderboard":
            screen_leaderboard()
        elif choice == "settings":
            screen_settings()

if __name__ == "__main__":
    main()
