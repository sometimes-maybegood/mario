import pygame
import random
import os
import sys


def st6():
    global WIDTH, Height, screen, screen_rect, all_sprites

    pygame.init()

    FPS = 50
    WIDTH = 600
    Height = 600
    screen = pygame.display.set_mode((WIDTH, Height))
    screen_rect = pygame.Rect(0, 0, WIDTH, Height)

    all_sprites = pygame.sprite.Group()

    Particle.initialize_fire()

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        create_random_particles()

        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


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
    fire = []

    @staticmethod
    def initialize_fire():
        Particle.fire.append(load_image("star.png"))
        for scale in (5, 10, 20):
            Particle.fire.append(pygame.transform.scale(Particle.fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = 1

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if not screen_rect.colliderect(self.rect):
            self.kill()


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def create_random_particles():
    if random.random() < 0.1:
        create_particles((random.randint(0, WIDTH), 0))


if __name__ == "__main__":
    try:
        os.system("python menu.py")
    except Exception as e:
        print(f"Ошибка при запуске menu.py: {e}")
        sys.exit(1)
