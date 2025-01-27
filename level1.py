import pygame
from PIL import Image

pygame.init()

W = 800
H = 600
screen = pygame.display.set_mode((W, H))

FPS = 60
clock = pygame.time.Clock()
STEP = 10
all_sprites = pygame.sprite.Group()
font_path = 'images/mario_font.ttf'
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

block_image = pygame.image.load('images/block.jpg')
block_image = pygame.transform.scale(block_image, (60, 60))
GROUND_H = block_image.get_height()

player_image = pygame.image.load('images/mario.png')
player_image = pygame.transform.scale(player_image, (60, 80))

coin_image = pygame.image.load('images/coin.png')
coin_image = pygame.transform.scale(coin_image, (30, 30))

flag_image = pygame.image.load('images/flag.png')
flag_image = pygame.transform.scale(flag_image, (60, 120))

img = Image.open('images/castle.jpg')
img = img.convert('RGBA')

new_img = Image.new('RGBA', img.size, (0, 0, 0, 0))

threshold = 240
for x in range(img.size[0]):
    for y in range(img.size[1]):
        pixel = img.getpixel((x, y))
        if pixel[0] < threshold or pixel[1] < threshold or pixel[2] < threshold:
            new_img.putpixel((x, y), pixel)

new_img.save('images/castle_no_bg.png')

castle_image_no_bg = pygame.image.load('images/castle_no_bg.png')
castle_image_no_bg = pygame.transform.scale(castle_image_no_bg, (500, 300))


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

            for block in ground_blocks:
                if self.rect.bottom > block[1] and self.rect.centerx > block[0] and self.rect.centerx < block[
                    0] + block_image.get_width():
                    self.is_grounded = True
                    self.y_speed = 0
                    self.rect.bottom = block[1]

            if self.rect.colliderect(
                    pygame.Rect(ladder_x, ladder_y, block_image.get_width(), block_image.get_height())):
                self.is_grounded = True
                self.y_speed = 0
                self.rect.bottom = ladder_y

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


class Castle(Entity):
    def __init__(self):
        super().__init__(castle_image_no_bg)
        self.rect.topleft = (W + 1400, H - GROUND_H - self.rect.height + 30)


castle = Castle()
player = Player()
camera = Camera(W, H)

castle_end_x = castle.rect.right

ground_blocks = []
for i in range(int((W + block_image.get_width()) / block_image.get_width()) * 4 + 1):
    for j in range(5):
        ground_x = i * block_image.get_width()
        ground_y = H - GROUND_H + j * block_image.get_height()

        if i >= 10 and i <= 15:
            ground_y -= 60
        elif i >= 20 and i <= 25:
            ground_y += 60

        ground_blocks.append((ground_x, ground_y))

ladder_x = 1000
ladder_y = H - GROUND_H - 300

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

    if player.rect.right >= castle_end_x:
        pygame.quit()
        exec(open('level3.py').read())

    camera.update(player)

    screen.fill((92, 148, 252))

    for block in ground_blocks:
        screen.blit(block_image, (block[0] - camera.x, block[1] - camera.y))

    screen.blit(block_image, (ladder_x - camera.x, ladder_y - camera.y))

    for i in range(int((W + block_image.get_width()) / block_image.get_width()) + 1):
        screen.blit(block_image, (i * block_image.get_width() - camera.x, H - GROUND_H - camera.y + 120))

    for i in range(int((W + block_image.get_width()) / block_image.get_width()) + 1):
        screen.blit(block_image, (i * block_image.get_width() - camera.x, H - GROUND_H - camera.y + 180))

    for i in range(int((W + block_image.get_width()) / block_image.get_width()) + 1):
        screen.blit(block_image, (i * block_image.get_width() - camera.x, H - GROUND_H - camera.y + 240))

    for i in range(int((W + block_image.get_width()) / block_image.get_width()) + 1):
        screen.blit(block_image, (i * block_image.get_width() - camera.x, H - GROUND_H - camera.y + 300))

    castle.draw(screen, camera)
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
