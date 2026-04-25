import pygame, sys
from pygame.locals import *
import random, time
import json

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

#Состояние звука
Sound = True

#Сложность
Difficulty = "Easy"
Difficulty_i = 0

#car colour
Car_colour = "Blue"
Car_colour_i = 0

# ник чтобы отображать в таблице лидеров
username = ""

nitro_active = False
nitro_start = 0

DISTANCE = 0

slow_active = False
slow_start = 0

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("images\AnimatedStreet.png")

# Создаём экран
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_leaderboard(leaderboard):
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)

#сохранение настроек       
def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except:
        return {"sound": True, "difficulty": "Easy", "car_colour": "Blue"}

def save_settings():
    with open("settings.json", "w") as f:
        json.dump({"sound": Sound, "difficulty": Difficulty, "car_colour": Car_colour}, f)
    
leaderboard = load_leaderboard()    
        
# рисуем кнопки для меню
def draw_button(text, x, y, w, h):
    pygame.draw.rect(DISPLAYSURF, (100, 100, 100), (x, y, w, h))
    txt = font_small.render(text, True, (255, 255, 255))
    DISPLAYSURF.blit(txt, (x + 10, y + 10))

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images\Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE, nitro_active
        # двигаем врага вниз
        self.rect.move_ip(0, SPEED)
        # если вышел за экран — возвращаем наверх и даём очко
        if self.rect.bottom > 600:
            SCORE += 2 if nitro_active else 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global Car_colour
        self.image = pygame.image.load(f"images\Player_{Car_colour}.png")
        self.image = pygame.transform.scale(self.image, (50, 100))
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
        # меняем размер
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        # монета падает вниз со скоростью SPEED
        self.rect.move_ip(0, SPEED)
        # если вышла за экран появляется снова сверху
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            


class Coin2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images\Power2.png")
        # меняем размер
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        # монета падает вниз со скоростью SPEED
        self.rect.move_ip(0, SPEED)
        # если вышла за экран появляется снова сверху
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            
class Coin3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images\Power3.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -1000)  
        self.spawn_time = time.time() + random.randint(10, 20)  #появится через 10-20 секунд

    def move(self):
        self.rect.move_ip(0, SPEED*1.5)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -3000)
            self.spawn_time = time.time() + random.randint(10, 20)
        
        # появляется только когда пришло время
        if time.time() >= self.spawn_time and self.rect.top < -500:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin4(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images\Shield.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -3000)  
        self.spawn_time = time.time() + random.randint(15, 30)  #появится через 15-30 секунд

    def move(self):
        self.rect.move_ip(0, SPEED*1.3)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -3000)
            self.spawn_time = time.time() + random.randint(15, 30)
        
        # появляется только когда пришло время
        if time.time() >= self.spawn_time and self.rect.top < -500:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin5(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images\Repair.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -3000)
        self.spawn_time = time.time() + random.randint(20, 40)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -3000)
            self.spawn_time = time.time() + random.randint(20, 40)
        if time.time() >= self.spawn_time and self.rect.top < -500:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class OilSpill(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images\oil.png")
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -1500)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -3000)

# Создаём спрайты
P1 = Player()
E1 = Enemy()
C1 = Coin1()
C2 = Coin2()
C3 = Coin3()
C4 = Coin4()
C5 = Coin5()
O1 = OilSpill()

# Группы спрайтов
enemies = pygame.sprite.Group()
coin1 = pygame.sprite.Group()
coin2 = pygame.sprite.Group()
coin3 = pygame.sprite.Group()
coin4 = pygame.sprite.Group()
coin5 = pygame.sprite.Group()
oil_spills = pygame.sprite.Group()

enemies.add(E1)
coin1.add(C1)
coin2.add(C2)
coin3.add(C3)
coin4.add(C4)
coin5.add(C5)
oil_spills.add(O1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
all_sprites.add(C2)
all_sprites.add(C3)
all_sprites.add(C4)
all_sprites.add(C5)
all_sprites.add(O1)

# Событие увеличения скорости каждую секунду
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Для отслеживания монет по которым +скорость
coins_speed = 0

#состояние
state = 'menu'

shield_active = False

settings = load_settings()
Sound = settings["sound"]
Difficulty = settings["difficulty"]
Car_colour = settings["car_colour"]

#ставим пониже чтобы применились настройки
P1 = Player()
all_sprites.empty()
all_sprites.add(O1, P1, E1, C1, C2, C3, C4, C5)

# Игровой цикл
while True:
    
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if state == 'username':
                if event.key == pygame.K_RETURN:
                        state = 'menu'
                elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                else:
                        username += event.unicode
                    
                    
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == 'menu':
                if pygame.Rect(161, 180, 95, 40).collidepoint(event.pos):
                    state = 'game'
                if pygame.Rect(161, 230, 95, 40).collidepoint(event.pos):
                    state = 'settings'
                if pygame.Rect(161, 280, 95, 40).collidepoint(event.pos):
                    state = 'quit'
                if pygame.Rect(100, 130, 200, 40).collidepoint(event.pos):
                    state = 'username'
                if pygame.Rect(257, -7, 150, 40).collidepoint(event.pos):
                    state = 'leaderboard'
                    
       
            elif state == 'settings': 
                if pygame.Rect(131, 180, 160, 40).collidepoint(event.pos):
                    Sound = not Sound
                    save_settings()
                if pygame.Rect(115, 230, 195, 40).collidepoint(event.pos):
                    Difficulty_i += 1
                    if Difficulty_i % 3 == 1:
                        Difficulty = "Medium"
                    elif Difficulty_i % 3 == 2:
                        Difficulty = "Hard"
                    else:
                        Difficulty = "Easy"
                    save_settings()
                if pygame.Rect(1, 1, 70, 40).collidepoint(event.pos):
                        state = 'menu'
                if pygame.Rect(115, 280, 195, 40).collidepoint(event.pos):
                    Car_colour_i += 1
                    if Car_colour_i % 3 == 1:
                        Car_colour = "Black"
                    elif Car_colour_i % 3 == 2:
                        Car_colour = "Green"
                    else:
                        Car_colour = "Blue"
                     # пересоздаём игрока с новым цветом
                    P1 = Player()
                    all_sprites.empty()
                    all_sprites.add(O1, P1, E1, C1, C2, C3, C4, C5) 
                    save_settings() 
                     
            elif state == 'username':
                if pygame.Rect(161, 310, 100, 35).collidepoint(event.pos):
                    state = 'menu'
                    
            elif state == 'leaderboard':
                if pygame.Rect(1, 1, 70, 40).collidepoint(event.pos):
                    state = 'menu'
                           
            elif state == 'gameover':
                
                    
                if pygame.Rect(155, 390, 100, 40).collidepoint(event.pos):
                    state = 'menu'
                    DISTANCE = 0
                    SCORE = 0
                    COINS = 0
                    SPEED = 5
                    coins_speed = 0
                    
                
                    P1 = Player()
                    E1 = Enemy()
                    C1 = Coin1()
                    C2 = Coin2()
                    C3 = Coin3()
                    C4 = Coin4()
                    C5 = Coin5()
                    O1 = OilSpill()
                    
                    
                    all_sprites.empty()
                    enemies.empty()
                    coin1.empty()
                    coin2.empty()
                    coin3.empty()
                    coin4.empty()
                    coin5.empty()
                    oil_spills.empty()
                    
                    enemies.add(E1)
                    coin1.add(C1)
                    coin2.add(C2)
                    coin3.add(C3)
                    coin4.add(C4)
                    coin5.add(C5)
                    oil_spills.add(O1)
                    all_sprites.add(O1, P1, E1, C1, C2, C3, C4, C5)
                    
                #Сбрасываем значения
                if pygame.Rect(155, 330, 100, 40).collidepoint(event.pos):
                    
                    SCORE = 0
                    DISTANCE = 0
                    COINS = 0
                    SPEED = 5
                    coins_speed = 0
                    
                
                    P1 = Player()
                    E1 = Enemy()
                    C1 = Coin1()
                    C2 = Coin2()
                    C3 = Coin3()
                    C4 = Coin4()
                    C5 = Coin5()
                    O1 = OilSpill()
                    
                    
                    all_sprites.empty()
                    enemies.empty()
                    coin1.empty()
                    coin2.empty()
                    coin3.empty()
                    coin4.empty()
                    coin5.empty()
                    oil_spills.empty()
                    
                    enemies.add(E1)
                    coin1.add(C1)
                    coin2.add(C2)
                    coin3.add(C3)
                    coin4.add(C4)
                    coin5.add(C5)
                    oil_spills.add(O1)
                    all_sprites.add(O1, P1, E1, C1, C2, C3, C4, C5)
                    
                    state = 'game'

    
    if state == 'menu':
        DISPLAYSURF.fill(BLACK)
        
        username1 = font_small.render(f"Player: {username}", True, WHITE)
        DISPLAYSURF.blit(username1, (0, 0))
        # рисуем кнопку 
        draw_button("Enter username: ", 100, 130, 200, 40)
        draw_button("Play", 161, 180, 95, 40)
        draw_button("Settings", 161, 230, 95, 40)
        draw_button("Quit", 161, 280, 95, 40)
        draw_button("Leaderboard", 257, -7, 150, 40)
    
    elif state == 'leaderboard':
        DISPLAYSURF.fill(BLACK)
        for i, entry in enumerate(leaderboard):
            txt = font_small.render(f"{i+1}. {entry['name']} - {entry['score']} | {entry.get('distance', 0)}m", True, WHITE)
            DISPLAYSURF.blit(txt, (100, 100 + 30*i))
        draw_button("Back", 1, 1, 70, 40)
        
    elif state == 'username':
        DISPLAYSURF.fill(BLACK)
        
        #вывод никнейма на экран
        txt = font_small.render("Enter username:", True, WHITE)
        DISPLAYSURF.blit(txt, (110, 200))
        pygame.draw.rect(DISPLAYSURF, WHITE, (110, 240, 200, 35), 2)
        
        name_txt = font_small.render(username, True, WHITE)
        DISPLAYSURF.blit(name_txt, (115, 245))
        draw_button("Confirm", 161, 310, 100, 35)
        
    elif state == 'settings':
        DISPLAYSURF.fill(BLACK)
        
        Sound_text = "Sound: On" if Sound else "Sound: Off"
        draw_button(Sound_text, 131, 180, 160, 40)
        draw_button(f"Difficulty: {Difficulty}", 115, 230, 195, 40)
        draw_button(f"Car colour: {Car_colour}", 115, 280, 195, 40)
        draw_button("Back", 1, 1, 70, 40)
        
    elif state == 'quit':
        pygame.quit()
        sys.exit()
    
    elif state == 'gameover':
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 150))
        score_txt = font_small.render(f"Score: {SCORE}", True, WHITE)
        coins_txt = font_small.render(f"Coins: {COINS}", True, WHITE)
        dist_txt = font_small.render(f"Distance: {int(DISTANCE)}m", True, WHITE)
        DISPLAYSURF.blit(score_txt, (130, 230))
        DISPLAYSURF.blit(coins_txt, (130, 255))
        DISPLAYSURF.blit(dist_txt, (130, 280))
        draw_button("Try again", 149, 330, 110, 40)
        draw_button("Menu", 155, 390, 100, 40)
        

    elif state == 'game':

        # фон
        DISPLAYSURF.blit(background, (0, 0))
        
        
        # счёт слева
        scores = font_small.render(f"Score: {SCORE}", True, BLACK)
        DISPLAYSURF.blit(scores, (10, 10))
        
        #показ остатка нитро в секундах
        if nitro_active:
            remaining = 5 - int(time.time() - nitro_start)
            nitro_txt = font_small.render(f"Nitro x2: {remaining}s", True, (0, 0, 0))
            DISPLAYSURF.blit(nitro_txt, (10, 35))
        else:
            nitro_txt = font_small.render(f"Nitro x2: OFF", True, (0, 0, 0))
            DISPLAYSURF.blit(nitro_txt, (10, 35))

        # счётчик монет справа
        coin_text = font_small.render(f"Coins: {COINS}", True, (0, 0, 0))
        DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 120, 10))
        
        #shield
        if shield_active:
            shield_txt = font_small.render("Shield: ON", True, BLUE)
            DISPLAYSURF.blit(shield_txt, (10, 80))
        else:
            shield_txt = font_small.render("Shield: OFF", True, BLUE)
            DISPLAYSURF.blit(shield_txt, (10, 80))

        # Двигаем и рисуем все спрайты
        for entity in all_sprites:
            entity.move()
            DISPLAYSURF.blit(entity.image, entity.rect)
            
        #дистанция   
        DISTANCE += SPEED/60
        dist_txt = font_small.render(f"Dist: {int(DISTANCE)}m", True, BLACK)
        DISPLAYSURF.blit(dist_txt, (10, 60))
            
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
            coin_hit2.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -2000)
            
        
        coin_hit3 = pygame.sprite.spritecollideany(P1, coin3)
        if coin_hit3:
            nitro_active = True
            nitro_start = time.time()
            coin_hit3.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -5000)
            
        if nitro_active and time.time() - nitro_start > 5:
            nitro_active = False
        
        
        coin_hit4 = pygame.sprite.spritecollideany(P1, coin4)
        if coin_hit4:
            shield_active = True
            coin_hit4.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -7000)
    
        coin_hit5 = pygame.sprite.spritecollideany(P1, coin5)
        if coin_hit5:
            shield_active = True
            coin_hit5.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -7000)
        
        #замедляем скорость при езде на масляной дороге
        oil_hit = pygame.sprite.spritecollideany(P1, oil_spills)
        if oil_hit:
            slow_active = True
            slow_start = time.time()
            oil_hit.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -3000)

        if slow_active:
            SPEED = max(2, SPEED - 0.05)  # замедляем но не ниже 2
            if time.time() - slow_start > 3:
                slow_active = False
    
        # +скорость за каждую десятую монету
        if (COINS % 10 == 0 or (COINS - 1) % 10 == 0) and COINS != 0 and COINS != coins_speed:
            if Difficulty == "Easy":
                SPEED += 0.05
            elif Difficulty == "Medium":
                SPEED += 0.1
            elif Difficulty == "Hard":
                SPEED += 0.5
            coins_speed += 10

        # Проверяем столкновение игрока с врагом
        if pygame.sprite.spritecollideany(P1, enemies):
            if shield_active:
                shield_active = False
                for enemy in enemies:
                    if enemy.rect.colliderect(P1.rect):
                        enemy.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            else:
                if Sound: 
                    pygame.mixer.Sound('sounds\crash.wav').play()
                #сохранение рекорда, если игрок не ввел никнейм то подбирается рандомный
                if username == "":
                    username = f"user{random.randint(10000, 99999)}"
                leaderboard.append({"name": username, "score": SCORE, "coins": COINS, "distance": int(DISTANCE)})
                leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
                save_leaderboard(leaderboard)
                
                state = 'gameover'
    

    pygame.display.update()
    FramePerSec.tick(FPS)