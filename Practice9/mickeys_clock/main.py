<<<<<<< HEAD
import pygame
import time
from clock import draw_clock

pygame.init()

w, h = 600, 600
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Clock")

clock = pygame.time.Clock()

bg = pygame.transform.scale(
    pygame.image.load("images\mickeyclock.jpeg"),
    (w, h)
)

center = (w // 2, h // 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t = time.localtime()
    minutes = t.tm_min
    seconds = t.tm_sec

    screen.blit(bg, (0, 0))

    draw_clock(screen, center, minutes, seconds)

    pygame.display.flip()
    clock.tick(60)

=======
import pygame
import time
from clock import draw_clock

pygame.init()

w, h = 600, 600
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Clock")

clock = pygame.time.Clock()

bg = pygame.transform.scale(
    pygame.image.load("images\mickeyclock.jpeg"),
    (w, h)
)

center = (w // 2, h // 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t = time.localtime()
    minutes = t.tm_min
    seconds = t.tm_sec

    screen.blit(bg, (0, 0))

    draw_clock(screen, center, minutes, seconds)

    pygame.display.flip()
    clock.tick(60)

>>>>>>> 7f5ccd649f15763808f59df31365b85eb5867a66
pygame.quit()