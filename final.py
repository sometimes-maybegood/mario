import pygame
import random
import os

FPS = 10
WIDTH = 600
Height = 600
screen = pygame.display.set_mode((WIDTH, Height))
screen_rect = (0, 0, WIDTH, Height)


def load_image(image_name, color_key=None):
    full_path = os.path.join('images', image_name)
    try:
        image = pygame.image.load(full_path)
    except pygame.error as message:
        print('Не удаётся загрузить:', image_name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 1

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
running = True

# Создаем частицы в случайных местах на экране
def create_random_particles():
    if random.random() < 0.1:  # 10% шанс создания частиц
        create_particles((random.randint(0, WIDTH), 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    create_random_particles()  # Создаем частицы в случайных местах

    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(50)

pygame.quit()
