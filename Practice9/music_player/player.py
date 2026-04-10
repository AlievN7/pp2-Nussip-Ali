import pygame
import os


pygame.mixer.init()


playlist = ["music/VHS.mp3", "music/007.mp3"]
current = 0
stop_count = 0

def play():
    global current
    pygame.mixer.music.load(playlist[current])
    pygame.mixer.music.play(loops = 0)
def stop():
    global stop_count
    stop_count += 1
    pygame.mixer.music.pause()
    if stop_count % 2 == 0:
        pygame.mixer.music.unpause()
def nexts():
    global current
    current += 1
    if current >= len(playlist):
        current -= len(playlist)
    pygame.mixer.music.load(playlist[current])
    pygame.mixer.music.play()
    
def back():
    global current
    current -= 1
    if -current >= len(playlist):
        current += len(playlist)
    pygame.mixer.music.load(playlist[current])
    pygame.mixer.music.play()
    
def quitt():
    pygame.quit()