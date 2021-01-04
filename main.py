import math
import pygame
import random
import traceback
import os, sys

size = width, height = 500, 500
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
tile_width = tile_height = 100
DELTA_V = 1


def load_level(filename):
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Floor(x, y)
            elif level[y][x] == '#':
                Floor(x, y)
                Asteroid(x, y)
            elif level[y][x] == '@':
                Floor(x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def load_image(name, colorkey=None):
    # если файл не существует, то выходим
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Floor(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(floor_group, all_sprites)
        self.image = tile_images["empty"]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(aster_group, all_sprites)
        self.image = random.choice(tile_images["wall"])
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 250
        self.dy = 250

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image["up"]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.vx = 0
        self.vy = 0

    def update(self, keys, *args):
        if keys[pygame.K_DOWN] or keys[pygame.K_UP] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            if keys[pygame.K_DOWN]:
                self.image = player_image["down"]
                self.vx, self.vy = 0, 10
            if keys[pygame.K_UP]:
                self.image = player_image["up"]
                self.vx, self.vy = 0, -10
            if keys[pygame.K_LEFT]:
                self.image = player_image["left"]
                self.vx, self.vy = -10, 0
            if keys[pygame.K_RIGHT]:
                self.image = player_image["right"]
                self.vx, self.vy = 10, 0
        else:
            if self.vx > 0:
                self.vx -= DELTA_V
                self.vx = 0 if self.vx <= 0 else self.vx
            if self.vx < 0:
                self.vx += DELTA_V
                self.vx = 0 if self.vx >= 0 else self.vx
            if self.vy > 0:
                self.vy -= DELTA_V
                self.vy = 0 if self.vy <= 0 else self.vy
            if self.vy < 0:
                self.vy += DELTA_V
                self.vy = 0 if self.vy >= 0 else self.vy
        if pygame.sprite.spritecollideany(self, aster_group):
            self.vy = 0
            self.vx = 0

        self.rect = self.rect.move(self.vx, self.vy)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
floor_group = pygame.sprite.Group()
aster_group = pygame.sprite.Group()

player_image = {"right": load_image("car_right.png"), "left": load_image("car_left.png"),
                "up": load_image("car_up.png"), "down": load_image("car_down.png")}

tile_images = {
    'wall': [load_image('obstacle.png'), load_image('obstacle2.png'), load_image('obstacle3.png')],
    'empty': load_image('floor.png')}
player, level_x, level_y = generate_level(load_level('map.txt'))
camera = Camera()
while running:
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill(pygame.Color('black'))
    key = pygame.key.get_pressed()
    player_group.update(key)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    floor_group.draw(screen)
    aster_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(50)

pygame.quit()
