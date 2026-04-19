<<<<<<< HEAD
import pygame
import math

def draw_clock(screen, center, minutes, seconds):

    sec_angle = seconds * 6
    min_angle = minutes * 6 + seconds * 0.1


    sec_length = 200
    min_length = 150

    sec_x = center[0] + sec_length * math.sin(math.radians(sec_angle))
    sec_y = center[1] - sec_length * math.cos(math.radians(sec_angle))

    pygame.draw.line(screen, (255, 0, 0), center, (sec_x, sec_y), 3)

    min_x = center[0] + min_length * math.sin(math.radians(min_angle))
    min_y = center[1] - min_length * math.cos(math.radians(min_angle))

=======
import pygame
import math

def draw_clock(screen, center, minutes, seconds):

    sec_angle = seconds * 6
    min_angle = minutes * 6 + seconds * 0.1


    sec_length = 200
    min_length = 150


    sec_x = center[0] + sec_length * math.sin(math.radians(sec_angle))
    sec_y = center[1] - sec_length * math.cos(math.radians(sec_angle))

    pygame.draw.line(screen, (255, 0, 0), center, (sec_x, sec_y), 3)

  
    min_x = center[0] + min_length * math.sin(math.radians(min_angle))
    min_y = center[1] - min_length * math.cos(math.radians(min_angle))

>>>>>>> 7f5ccd649f15763808f59df31365b85eb5867a66
    pygame.draw.line(screen, (0, 0, 0), center, (min_x, min_y), 6)