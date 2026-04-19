import pygame

def UP(x, y):
    return x, y - 20
    
def RIGHT(x, y):
    return x + 20, y

def LEFT(x, y):
    return x - 20, y    
    
def DOWN(x, y):
    return x, y + 20