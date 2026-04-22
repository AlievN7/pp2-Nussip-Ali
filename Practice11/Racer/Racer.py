import pygame, sys
from pygame.locals import *
import random, time

# Инициализация pygame
pygame.init()

# Настройка FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Переменные
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("images\AnimatedStreet.png")

# Создаём экран
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images\Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        # двигаем врага вниз
        self.rect.move_ip(0, SPEED)
        # если вышел за экран — возвращаем наверх и даём очко
        if self.rect.bottom > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images\Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # двигаем игрока влево/вправо не выходя за границы
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


class Coin1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images\Power1.png")
        # масштабируем монету до нужного размера
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        # монета падает вниз со скоростью SPEED
        self.rect.move_ip(0, SPEED)
        # если вышла за экран — появляется снова сверху
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            


class Coin2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images\Power2.png")
        # масштабируем монету до нужного размера
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        # монета падает вниз со скоростью SPEED
        self.rect.move_ip(0, SPEED)
        # если вышла за экран — появляется снова сверху
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


# Создаём спрайты
P1 = Player()
E1 = Enemy()
C1 = Coin1()
C2 = Coin2()

# Группы спрайтов
enemies = pygame.sprite.Group()
coin1 = pygame.sprite.Group()
coin2 = pygame.sprite.Group()
enemies.add(E1)
coin1.add(C1)
coin2.add(C2)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
all_sprites.add(C2)

# Событие увеличения скорости каждую секунду
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Для отслеживания монет по которым +скорость
coins_speed = 0

# Игровой цикл
while True:

    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.125
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # фон
    DISPLAYSURF.blit(background, (0, 0))

    # счёт слева
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # счётчик монет справа
    coin_text = font_small.render(f"Coins: {COINS}", True, (0, 0, 0))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 120, 10))

    # Двигаем и рисуем все спрайты
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Проверяем столкновение игрока с монетой
    coin_hit1 = pygame.sprite.spritecollideany(P1, coin1)
    if coin_hit1:
        COINS += 1
        # перемещаем монету в новое место
        coin_hit1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        
    
    coin_hit2 = pygame.sprite.spritecollideany(P1, coin2)
    if coin_hit2:
        COINS += 2
        # перемещаем монету в новое место
        coin_hit2.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        
    # +скорость за каждую десятую монету
    if (COINS % 10 == 0 or (COINS - 1) % 10 == 0) and COINS != 0 and COINS != coins_speed:
        SPEED += 0.125
        coins_speed += 10

    # Проверяем столкновение игрока с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('sounds\crash.wav').play()
        time.sleep(1)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)