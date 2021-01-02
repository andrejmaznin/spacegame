import math
import pygame
import traceback
import os, sys

size = width, height = 501, 501
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption('Перемещение')
running = True
rect_width = 0
rect_x = 0
rect_y = 0
square_width = 100
col = pygame.Color('red')
rect_rect = ((rect_x, rect_y), (square_width, square_width))
x_prev = x2 = y_prev = y2 = 0
dest = []
x = y = 250


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def load_image(name, colorkey=None):
    # если файл не существует, то выходим
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    return image


class MainHero(pygame.sprite.Sprite):

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(*group)
        self.image = load_image("car1.png")
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 250

    def update(self, keys, *args):
        if keys[pygame.K_DOWN]:
            self.rect = self.rect.move(0, 10)
        if keys[pygame.K_UP]:
            self.rect = self.rect.move(0, -10)
        if keys[pygame.K_LEFT]:
            self.rect = self.rect.move(-10, 0)
        if keys[pygame.K_RIGHT]:
            self.rect = self.rect.move(10, 0)


all_sprites = pygame.sprite.Group()

# создадим спрайт

MainHero(all_sprites)

while running:
    screen.fill(pygame.Color('black'))
    key = pygame.key.get_pressed()
    if key[pygame.K_DOWN] or key[pygame.K_UP] or key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
        all_sprites.update(key)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(100)

pygame.quit()
