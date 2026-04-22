import pygame, sys
import random
import time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (117, 124, 136)

# Размеры экрана и сегмента змейки
w = 600
h = 400

# Переменные игры
SPEED = 7
SCORE = 0
LEVEL = 1
SEG = 20

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over_text = font.render("Game Over", True, BLACK)

# Экран
display = pygame.display.set_mode((w, h))
pygame.display.set_caption("Snake")

food1_img = pygame.image.load("images\power.png")
food1_img = pygame.transform.scale(food1_img, (SEG, SEG))

food2_img = pygame.image.load(r"images\food2.png")
food2_img = pygame.transform.scale(food2_img, (SEG, SEG))


def spawn_food(snake):
    # генерируем еду пока она не окажется вне змейки
    while True:
        fx = random.randint(0, (w // SEG) - 1) * SEG
        fy = random.randint(0, (h // SEG) - 1) * SEG
        if (fx, fy) not in snake:
            return fx, fy


# Начальное состояние змейки
snake = [(w//2, h//2), (w//2 - SEG, h//2), (w//2 - SEG*2, h//2)]
Direction = "RIGHT"

# Первая еда
food1_x, food1_y = spawn_food(snake)
food1_rect = food1_img.get_rect()
food1_rect.topleft = (food1_x, food1_y)

# Bторая
food2_x, food2_y = spawn_food(snake)
food2_rect = food2_img.get_rect()
food2_rect.topleft = (food2_x, food2_y)

start_time = time.time()


# Игровой цикл
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # меняем направление, запрещаем разворот на 180 градусов
            if (event.key == pygame.K_w or event.key == pygame.K_UP) and Direction != "DOWN":
                Direction = "UP"
            elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and Direction != "UP":
                Direction = "DOWN"
            elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and Direction != "RIGHT":
                Direction = "LEFT"
            elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and Direction != "LEFT":
                Direction = "RIGHT"

    # Вычисляем новую голову
    head_x, head_y = snake[0]

    if Direction == "UP":
        head_y -= SEG
    elif Direction == "DOWN":
        head_y += SEG
    elif Direction == "LEFT":
        head_x -= SEG
    elif Direction == "RIGHT":
        head_x += SEG

    new_head = (head_x, head_y)

    # Проверка столкновения со стеной
    if head_x < 0 or head_x >= w or head_y < 0 or head_y >= h:
        display.fill(RED)
        display.blit(game_over_text, (w//2 - 150, h//2 - 50))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    # Проверка столкновения с собой
    if new_head in snake:
        display.fill(RED)
        display.blit(game_over_text, (w//2 - 150, h//2 - 50))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    # Добавляем новую голову
    snake.insert(0, new_head)

    current_time = time.time() - start_time
    
    if current_time >= 5:
        food2_x, food2_y = spawn_food(snake)
        food2_rect.topleft = (food2_x, food2_y)
        start_time = time.time()
    
    # Проверяем съела ли змейка первую еду
    if new_head == (food1_x, food1_y):
        SCORE += 1
        # каждые 3 очка новый уровень
        if SCORE % 3 == 0:
            LEVEL += 1
            SPEED += 1
        food1_x, food1_y = spawn_food(snake)
        food1_rect.topleft = (food1_x, food1_y)
    #проверка на вторую еду    
    elif new_head == (food2_x, food2_y):
        SCORE += 5
        if SCORE % 3 == 0:
            LEVEL += 1
            SPEED += 1
        food2_x, food2_y = spawn_food(snake)
        food2_rect.topleft = (food2_x, food2_y)
        
    else:
        # удаляем хвост
        snake.pop()

    
    display.fill(GRAY)

    # рисуем каждый сегмент змейки
    for segment in snake:
        pygame.draw.rect(display, GREEN, [segment[0], segment[1], SEG, SEG])

    display.blit(food1_img, food1_rect)
    display.blit(food2_img, food2_rect)

    # Счёт и уровень
    score_text = font_small.render(f"Score: {SCORE}  Level: {LEVEL}", True, BLACK)
    display.blit(score_text, (10, 10))

    pygame.display.update()
    FramePerSec.tick(SPEED)