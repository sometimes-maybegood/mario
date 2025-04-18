import pygame
from PIL import Image
from level3 import st2


def st1():
    pygame.init()
    global W, H, screen, FPS, clock, STEP, all_sprites, font_path, font_large, font_small, INIT_DELAY
    global spawn_delay, DECREASE_BASE, last_spawn_time, game_over, retry_text, retry_rect, score
    global block_image, GROUND_H, player_image, coin_image, img, new_img, pixel, threshold
    global castle_image_no_bg, player, castle, camera, castle_end_x, ladder_x, ladder_y, ground_blocks
    global ground_x, ground_y, running, score_rect, score_surface, finish_delay, coin_block_image, img1, new_img1, pixel1
    global coin_image, coins, coin_blocks, solid_blocks, ladder_blocks
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
    for x in range(img1.size[0]):
        for y in range(img1.size[1]):
            pixel1 = img1.getpixel((x, y))
            if pixel1[0] < threshold or pixel1[1] < threshold or pixel1[2] < threshold:
                new_img1.putpixel((x, y), pixel1)

    new_img1.save('images/coin_new.png')

    coin_image = pygame.image.load('images/coin_new.png')
    coin_image = pygame.transform.scale(coin_image, (50, 30))
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

    ladder_blocks = []
    ladder_x = 1000
    ladder_y = H - GROUND_H
    for i in range(4):
        ladder_blocks.append((ladder_x, ladder_y - i * block_image.get_height()))

    coin_blocks = []
    for i in range(5):
        coin_x = 1200 + i * block_image.get_width()
        coin_y = H - GROUND_H - 3 * block_image.get_height()
        coin_blocks.append((coin_x, coin_y))

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
            st2()

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

        for i in range(int((W + block_image.get_width()) / block_image.get_width()) + 1):
            screen.blit(block_image, (i * block_image.get_width() - camera.x, H - GROUND_H - camera.y + 120))

        for i in range(int((W + block_image.get_width()) / block_image.get_width()) + 1):
            screen.blit(block_image, (i * block_image.get_width() - camera.x, H - GROUND_H - camera.y + 180))

        for i in range(int((W + block_image.get_width()) / block_image.get_width()) * 2 + 1):
            screen.blit(block_image, (i * block_image.get_width() - camera.x, H - GROUND_H - camera.y + 240))

        for i in range(int((W + block_image.get_width()) / block_image.get_width()) * 3 + 1):
            screen.blit(block_image, (i * block_image.get_width() - camera.x, H - GROUND_H - camera.y + 300))

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

    def jump(self):
        self.y_speed = self.jump_speed


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
        self.rect.topleft = (W + 1400, H - GROUND_H - self.rect.height + 30)



