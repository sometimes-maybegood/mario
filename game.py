import pygame
pygame.init()

W = 800
H = 600
screen = pygame.display.set_mode((W, H))

FPS = 60
clock = pygame.time.Clock()

font_path = 'mario_font.ttf'
font_large = pygame.font.Font(font_path, 48)
font_small = pygame.font.Font(font_path, 24)