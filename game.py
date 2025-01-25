import pygame
from rembg.bg import remove
import numpy as np
import io
from PIL import Image

pygame.init()

W = 800
H = 600
screen = pygame.display.set_mode((W, H))

FPS = 60
clock = pygame.time.Clock()
STEP = 10
all_sprites = pygame.sprite.Group()
font_path = 'mario_font.ttf'
font_large = pygame.font.Font(font_path, 48)
font_small = pygame.font.Font(font_path, 24)
INIT_DELAY = 2000
spawn_delay = INIT_DELAY
DECREASE_BASE = 1.01
last_spawn_time = pygame.time.get_ticks()

game_over = False
retry_text = font_small.render('PRESS ANY KEY', True, (255, 255, 255))
retry_rect = retry_text.get_rect()
retry_rect.midtop = (W // 2, H // 2)

score = 0

ground_image = pygame.image.load('ground.png')
ground_image = pygame.transform.scale(ground_image, (804, 60))
GROUND_H = ground_image.get_height()

player_image = pygame.image.load('mario.png')
player_image = pygame.transform.scale(player_image, (60, 80))

coin_image = pygame.image.load('coin.png')
coin_image = pygame.transform.scale(coin_image, (30, 30))

flag_image = pygame.image.load('flag.png')
flag_image = pygame.transform.scale(flag_image, (60, 120))

input_path = 'castle.jpg'
output_path = 'castle_no_bg.png'

f = np.fromfile(input_path)
result = remove(f)
img = Image.open(io.BytesIO(result)).convert("RGBA")
img.save(output_path)

castle_image_no_bg = pygame.image.load('castle_no_bg.png')
castle_image_no_bg = pygame.transform.scale(castle_image_no_bg, (60, 60))


class Entity:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.y_speed = 0
        self.x_speed = 0
        self.speed = 5
        self.is_out = False
        self.is_dead = False
        self.jump_speed = -12
        self.gravity = 0.5
        self.is_grounded = False

    def handle_input(self):
        pass

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        self.y_speed += self.gravity

        if self.is_dead:
            if self.rect.top > H - GROUND_H:
                self.is_out = True
        else:
            self.handle_input()

            if self.rect.bottom > H - GROUND_H:
                self.is_grounded = True
                self.y_speed = 0
                self.rect.bottom = H - GROUND_H

    def draw(self, surface, camera):
        surface.blit(self.image, (self.rect.x - camera.x, self.rect.y - camera.y))


class Player(Entity):
    def __init__(self):
        super().__init__(player_image)
        self.respawn()

    def handle_input(self):
        self.x_speed = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_speed = -self.speed
        elif keys[pygame.K_d]:
            self.x_speed = self.speed

        if self.rect.x + self.x_speed < 0:
            self.x_speed = -self.rect.x

        if self.is_grounded and keys[pygame.K_SPACE]:
            self.is_grounded = False
            self.jump()

    def respawn(self):
        self.is_out = False
        self.is_dead = False
        self.rect.midbottom = (W // 2, H)

    def jump(self):
        self.y_speed = self.jump_speed


class Coin(Entity):
    def __init__(self, x, y):
        super().__init__(coin_image)
        self.rect.topleft = (x, y)


class Flag(Entity):
    def __init__(self):
        super().__init__(flag_image)
        self.rect.topleft = (W - 100, H - GROUND_H - self.rect.height)


class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

    def update(self, target):
        self.x = target.rect.centerx - self.width // 2
        self.y = target.rect.centery - self.height // 2


player = Player()
camera = Camera(W, H)

running = True

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if player.is_out:
                score = 0
                finish_delay = INIT_DELAY
                last_spawn_time = pygame.time.get_ticks()
                player.respawn()

    clock.tick(FPS)

    player.update()

    camera.update(player)

    screen.fill((92, 148, 252))

    for i in range(int((W + ground_image.get_width()) / ground_image.get_width()) * 4 + 1):
        screen.blit(ground_image, (i * ground_image.get_width() - camera.x, H - GROUND_H - camera.y))

    for i in range(int((W + ground_image.get_width()) / ground_image.get_width()) * 4 + 1):
        screen.blit(ground_image, (i * ground_image.get_width() - camera.x, H - GROUND_H - camera.y + 60))

    for i in range(int((W + ground_image.get_width()) / ground_image.get_width()) * 4 + 1):
        screen.blit(ground_image, (i * ground_image.get_width() - camera.x, H - GROUND_H - camera.y + 120))

    for i in range(int((W + ground_image.get_width()) / ground_image.get_width()) * 4 + 1):
        screen.blit(ground_image, (i * ground_image.get_width() - camera.x, H - GROUND_H - camera.y + 180))

    for i in range(int((W + ground_image.get_width()) / ground_image.get_width()) * 4 + 1):
        screen.blit(ground_image, (i * ground_image.get_width() - camera.x, H - GROUND_H - camera.y + 240))

    player.draw(screen, camera)

    score_surface = font_large.render(str(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect()
    score_rect.midtop = (W // 2, 5)

    screen.blit(score_surface, score_rect)

    if player.is_out:
        retry_rect.midtop = (W // 2, H // 2)
        screen.blit(retry_text, retry_rect)

    pygame.display.flip()

pygame.quit()
