import pygame
from PIL import Image
from random import randint
from level6 import st5

goombas = []


def st4():
    pygame.init()
    global W, H, screen, FPS, clock, STEP, all_sprites, font_path, font_large, font_small, INIT_DELAY
    global spawn_delay, DECREASE_BASE, last_spawn_time, game_over, retry_text, retry_rect, score
    global block_image, GROUND_H, player_image, coin_image, img, new_img, pixel, threshold
    global castle_image_no_bg, player, castle, camera, castle_end_x, ladder_x, ladder_y, ground_blocks
    global ground_x, ground_y, running, score_rect, score_surface, finish_delay, coin_block_image, img1, new_img1, pixel1
    global coin_image, coins, coin_blocks, solid_blocks, ladder_blocks
    global goomba_image, fireball_image, lasers, goombas
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

    try:
        with open('score.txt', 'r') as f:
            score = int(f.read())
    except FileNotFoundError:
        score = 0

    block_image = pygame.image.load('images/block.jpg')
    block_image = pygame.transform.scale(block_image, (60, 60))
    GROUND_H = block_image.get_height()

    coin_block_image = pygame.image.load('images/coin_block.jpg')
    coin_block_image = pygame.transform.scale(coin_block_image, (60, 60))

    player_image = pygame.image.load('images/mario.png')
    player_image = pygame.transform.scale(player_image, (50, 75))

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

    img1 = Image.open('images/coin.png')
    img1 = img1.convert('RGBA')

    new_img1 = Image.new('RGBA', img1.size, (0, 0, 0, 0))

    threshold = 240
    for x in range(img1.size[0]):
        for y in range(img1.size[1]):
            pixel1 = img1.getpixel((x, y))
            if pixel1[0] < threshold or pixel1[1] < threshold or pixel1[2] < threshold:
                new_img1.putpixel((x, y), pixel1)

    new_img1.save('images/coin_new.png')

    coin_image = pygame.image.load('images/coin_new.png')
    coin_image = pygame.transform.scale(coin_image, (50, 30))

    img2 = Image.open('images/goomba.jpg')
    img2 = img2.convert('RGBA')

    new_img2 = Image.new('RGBA', img2.size, (0, 0, 0, 0))

    threshold = 240
    for x in range(img2.size[0]):
        for y in range(img2.size[1]):
            pixel2 = img2.getpixel((x, y))
            if pixel2[0] < threshold or pixel2[1] < threshold or pixel2[2] < threshold:
                new_img2.putpixel((x, y), pixel2)

    new_img2.save('images/goomba_new.png')

    goomba_image = pygame.image.load('images/goomba_new.png')
    goomba_image = pygame.transform.scale(goomba_image, (40, 40))

    img3 = Image.open('images/fireball.jpg')
    img3 = img3.convert('RGBA')

    new_img3 = Image.new('RGBA', img3.size, (0, 0, 0, 0))

    threshold = 240
    for x in range(img3.size[0]):
        for y in range(img3.size[1]):
            pixel3 = img3.getpixel((x, y))
            if pixel3[0] < threshold or pixel3[1] < threshold or pixel3[2] < threshold:
                new_img3.putpixel((x, y), pixel3)

    new_img3.save('images/fireball_new.png')

    fireball_image = pygame.image.load('images/fireball_new.png')
    fireball_image = pygame.transform.scale(fireball_image, (30, 30))

    castle = Castle()
    player = Player()
    camera = Camera(W, H)

    castle_end_x = castle.rect.right

    ground_blocks = []
    for i in range(int((W + block_image.get_width()) / block_image.get_width()) * 6 + 1):
        for j in range(5):
            ground_x = i * block_image.get_width()
            ground_y = H - GROUND_H + j * block_image.get_height()

            if i >= 10 and i <= 15:
                ground_y -= 60
            elif i >= 20 and i <= 25:
                ground_y += 60
            elif i >= 30 and i <= 35:
                ground_y -= 120
            elif i >= 40 and i <= 45:
                ground_y += 120

            ground_blocks.append((ground_x, ground_y))

    ladder_blocks = []
    ladder_x = 1000
    ladder_y = H - GROUND_H
    for i in range(4):
        ladder_blocks.append((ladder_x, ladder_y - i * block_image.get_height()))

    coin_blocks = []
    for i in range(6):
        coin_x = 1200 + i * block_image.get_width()
        coin_y = H - GROUND_H - 3 * block_image.get_height()
        coin_blocks.append((coin_x, coin_y))

    goombas = []
    for i in range(8):
        goomba_x = 1500 + i * 200
        goomba_y = H - GROUND_H - goomba_image.get_height()
        path = (1610 + i * 200, 1755 + i * 200)
        goombas.append(Goomba(goomba_x, goomba_y, path))

    lasers = []
    laser_x = W + 2000
    laser_y = H // 2
    lasers.append(Laser(laser_x, laser_y, randint(2, 5)))

    solid_blocks = []
    coins = []

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
            with open('score.txt', 'w') as f:
                f.write(str(score))
            pygame.quit()
            st5()

        camera.update(player)

        screen.fill((92, 148, 252))

        for block in ground_blocks:
            screen.blit(block_image, (block[0] - camera.x, block[1] - camera.y))

        for ladder_block in ladder_blocks:
            screen.blit(block_image, (ladder_block[0] - camera.x, ladder_block[1] - camera.y))

        for coin_block in coin_blocks:
            screen.blit(coin_block_image, (coin_block[0] - camera.x, coin_block[1] - camera.y))

        for solid_block in solid_blocks:
            screen.blit(block_image, (solid_block[0] - camera.x, solid_block[1] - camera.y))

        for coin in coins:
            screen.blit(coin_image, (coin[0] - camera.x, coin[1] - camera.y))

        for goomba in goombas:
            goomba.update()
            if player.rect.colliderect(goomba.rect):
                if player.y_speed > 0 and player.rect.bottom <= goomba.rect.top + 10:
                    goombas.remove(goomba)
                    player.y_speed = -player.jump_speed / 2
                else:
                    player.is_out = True

        for goomba in goombas:
            screen.blit(goomba.image, (goomba.rect.x - camera.x, goomba.rect.y - camera.y))

        for laser in lasers:
            laser.update()
            if laser.fireballs[0][0] < 0:
                laser.fireballs = []
                laser_x = W + 2000
                laser_y = H // 2
                lasers[0] = Laser(laser_x, laser_y, randint(2, 5))

        for laser in lasers:
            laser.draw(screen, camera)

        for i in range(int((W + block_image.get_width()) + 1)):
            screen.blit(block_image, (i * block_image.get_width() - camera.x, H - GROUND_H - camera.y + 120))

        for i in range(int((W + block_image.get_width()) + 1)):
            screen.blit(block_image, (i * block_image.get_width() - camera.x, H - GROUND_H - camera.y + 180))

        for i in range(int((W + block_image.get_width()) + 1)):
            screen.blit(block_image, (i * block_image.get_width() - camera.x, H - GROUND_H - camera.y + 240))

        for i in range(int((W + block_image.get_width()) + 1)):
            screen.blit(block_image, (i * block_image.get_width() - camera.x, H - GROUND_H - camera.y + 300))

        for i in range(int((W + block_image.get_width()) * 2 + 1)):
            screen.blit(block_image, (i * block_image.get_width() - camera.x, H - GROUND_H - camera.y + 360))

        castle.draw(screen, camera)
        player.draw(screen, camera)

        for coin in coins[:]:
            if player.rect.colliderect(pygame.Rect(coin[0], coin[1], coin_image.get_width(), coin_image.get_height())):
                coins.remove(coin)
                score += 1

        score_surface = font_large.render(str(score), True, (255, 255, 255))
        score_rect = score_surface.get_rect()
        score_rect.midtop = (W // 2, 5)

        screen.blit(score_surface, score_rect)

        if player.is_out:
            retry_rect.midtop = (W // 2, H // 2)
            screen.blit(retry_text, retry_rect)
        pygame.display.flip()

    pygame.quit()


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
            for block in ground_blocks + ladder_blocks + solid_blocks:
                if self.rect.colliderect(
                        pygame.Rect(block[0], block[1], block_image.get_width(), block_image.get_height())):
                    if self.y_speed > 0:
                        self.is_grounded = True
                        self.y_speed = 0
                        self.rect.bottom = block[1]
                    elif self.y_speed < 0:
                        self.y_speed = 0
                        self.rect.top = block[1] - self.rect.height

            for coin_block in coin_blocks:
                if self.rect.colliderect(
                        pygame.Rect(coin_block[0], coin_block[1], block_image.get_width(), block_image.get_height())):
                    if self.y_speed < 0:
                        coins.append(
                            (coin_block[0] + block_image.get_width() // 2, coin_block[1] - coin_image.get_height()))
                        coin_blocks.remove(coin_block)
                        solid_blocks.append((coin_block[0], coin_block[1]))

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
        self.y_speed = 0
        self.x_speed = 0

        global coin_blocks
        coin_blocks = []
        for i in range(6):
            coin_x = 1200 + i * block_image.get_width()
            coin_y = H - GROUND_H - 3 * block_image.get_height()
            coin_blocks.append((coin_x, coin_y))

        global coins, solid_blocks
        coins = []
        solid_blocks = []

        global goombas
        goombas = []
        for i in range(8):
            goomba_x = 1500 + i * 200
            goomba_y = H - GROUND_H - goomba_image.get_height()
            path = (1610 + i * 200, 1755 + i * 200)
            goombas.append(Goomba(goomba_x, goomba_y, path))

    def jump(self):
        self.y_speed = self.jump_speed

    def update(self):
        super().update()

        global score
        for goomba in goombas[:]:
            if self.rect.colliderect(goomba.rect):
                if self.y_speed > 0 and self.rect.bottom <= goomba.rect.top + 10:
                    goombas.remove(goomba)
                    self.y_speed = -self.jump_speed / 2
                    score += 1
                else:
                    self.is_out = True

        for laser in lasers:
            for fireball_x, fireball_y in laser.fireballs:
                if self.rect.colliderect(
                        pygame.Rect(fireball_x, fireball_y, fireball_image.get_width(), fireball_image.get_height())):
                    self.is_out = True

        if self.rect.bottom > H + 100:
            self.is_out = True


class Laser:
    def __init__(self, x, y, num_fireballs):
        self.fireballs = []
        for i in range(num_fireballs):
            fireball_x = x + i * fireball_image.get_width()
            fireball_y = y
            self.fireballs.append((fireball_x, fireball_y))

    def update(self):
        for i, (fireball_x, fireball_y) in enumerate(self.fireballs):
            self.fireballs[i] = (fireball_x - 5, fireball_y)

    def draw(self, surface, camera):
        for fireball_x, fireball_y in self.fireballs:
            surface.blit(fireball_image, (fireball_x - camera.x, fireball_y - camera.y))


class Goomba(Entity):
    def __init__(self, x, y, path):
        super().__init__(goomba_image)
        self.rect.topleft = (x, y)
        self.speed = 1
        self.path = path
        self.direction = -1

    def handle_input(self):
        self.x_speed = self.speed * self.direction

    def update(self):
        super().update()
        self.rect.x += self.x_speed

        for block in ground_blocks + ladder_blocks + solid_blocks:
            if self.rect.colliderect(
                    pygame.Rect(block[0], block[1], block_image.get_width(), block_image.get_height())):
                if self.y_speed > 0:
                    self.y_speed = 0
                    self.rect.bottom = block[1]
                elif self.y_speed < 0:
                    self.y_speed = 0
                    self.rect.top = block[1] - self.rect.height

        if self.rect.left < self.path[0]:
            self.speed = -1
        elif self.rect.right > self.path[1]:
            self.speed = 1


class Coin(Entity):
    def __init__(self, x, y):
        super().__init__(coin_image)
        self.rect.topleft = (x, y)


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
        self.rect.topleft = (W + 2200, H - GROUND_H - self.rect.height + 30)
