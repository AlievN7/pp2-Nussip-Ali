import pygame

pygame.init()
h, w = 900, 600
screen = pygame.display.set_mode((h,w))
pygame.display.set_caption("Resident Evil Requiem")
icon = pygame.image.load('images/rree99icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
x, y = 15, 15

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP] or keys[pygame.K_w]:
            x, y = x, y - 10 
            
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x, y = x + 10, y
            
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            x, y = x, y + 10
            
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x, y = x - 10, y
            
    if x > w:
        x = w
    if y > h:
        y = h

            
    p1 = pygame.draw.line(screen, 'Blue', (x, y),(x, y + 20), 10)
    
    pygame.display.flip()
    clock.tick(60)