<<<<<<< HEAD
import pygame
import movingball


pygame.init()


screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Moving Ball")

clock = pygame.time.Clock()
radius = 25
x, y = 90, 90

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP] or keys[pygame.K_w]:
            x, y = movingball.UP(x, y)
            
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x, y = movingball.RIGHT(x, y)
            
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            x, y = movingball.DOWN(x, y)
            
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x, y = movingball.LEFT(x, y)

    if x < radius:
        x = radius
    if x > 900 - radius:
        x = 900 - radius
    if y < radius:
        y = radius
    if y > 600 - radius:
        y = 600 - radius
            
    screen.fill((255, 255, 255))
    
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)
    
    pygame.display.flip()
    clock.tick(60)
    

=======
import pygame
import ball


pygame.init()


screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Moving Ball")

clock = pygame.time.Clock()
radius = 25
x, y = 90, 90

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP] or keys[pygame.K_w]:
            x, y = ball.UP(x, y)
            
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x, y = ball.RIGHT(x, y)
            
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            x, y = ball.DOWN(x, y)
            
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x, y = ball.LEFT(x, y)

    if x < radius:
        x = radius
    if x > 900 - radius:
        x = 900 - radius
    if y < radius:
        y = radius
    if y > 600 - radius:
        y = 600 - radius
            
    screen.fill((255, 255, 255))
    
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)
    
    pygame.display.flip()
    clock.tick(60)
    

>>>>>>> 7f5ccd649f15763808f59df31365b85eb5867a66
pygame.quit()