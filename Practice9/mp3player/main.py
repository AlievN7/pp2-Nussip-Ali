import pygame
import os
from mutagen.mp3 import MP3
import player

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("MP3 Player")
font = pygame.font.Font(None, 36)

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.nexts()
            elif event.key == pygame.K_b:
                player.back()
            elif event.key == pygame.K_q:
                player.quitt()
    
    screen.fill((30, 30, 30))
    
    current_track_name = os.path.basename(player.playlist[player.current])
    text_surface = font.render(current_track_name, True, (255, 255, 255))
    screen.blit(text_surface, (50, 30))
    
    
    try:
        track_path = player.playlist[player.current]
        audio = MP3(track_path)
        duration = audio.info.length  
        pos_sec = pygame.mixer.music.get_pos() / 1000  
        progress = min(pos_sec / duration, 1)

        slider_x = 50
        slider_y = 100
        slider_width = 400
        slider_height = 10


        pygame.draw.rect(screen, (100, 100, 100), (slider_x, slider_y, slider_width, slider_height))

        pygame.draw.rect(screen, (0, 200, 0), (slider_x, slider_y, slider_width * progress, slider_height))

    except Exception as e:
        pass  

    pygame.display.update()