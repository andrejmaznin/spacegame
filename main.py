import math
import pygame
import random
import traceback
import os
import sys

size = 500, 500
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
infoObject = pygame.display.Info()
width, height = infoObject.current_w, infoObject.current_h
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
V = 20


def load_level(filename):
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_map(filename):
    with open(filename, 'w') as mapFile:
        a = [["." for i in range(50)] for j in range(50)]
        a[25][25] = "S"
        for i in range(random.randint(1, 10)):
            a[random.randint(4, 45)][random.randint(4, 45)] = "P"
        a[49][24] = "@"

        a = "".join(["".join(i) + "\n" for i in a])
        mapFile.write(a)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'S':
                Floor(x, y)
                Star(x, y)
            elif level[y][x] == ".":
                Floor(x, y)
            elif level[y][x] == 'P':
                Floor(x, y)
                Planet(x, y)
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
    def __init__(self, pos_x, pos_y, columns=8, rows=8):
        super().__init__(floor_group, all_sprites)
        self.frames = []
        self.cur_frame = random.randint(0, 63)
        self.cut_sheet(tile_images["empty"], columns, rows)
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)

        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))


class Planet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(planet_group, all_sprites)
        self.image = tile_images["planet"]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Star(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(star_group, all_sprites)
        self.image = tile_images["sun"]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = width // 2
        self.dy = height // 2

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, columns=8, rows=1):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.cur_frame = 3
        self.cut_sheet(player_image, columns, rows)
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)

        self.vx = 0
        self.vy = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, keys, *args):
        if keys[pygame.K_DOWN] or keys[pygame.K_UP] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            if keys[pygame.K_DOWN]:
                self.cur_frame = 0
                self.vy = self.vy + DELTA_V if self.vy + DELTA_V <= V else V
                self.vx = 0
            if keys[pygame.K_UP]:
                self.cur_frame = 3

                self.vy = self.vy - DELTA_V if self.vy - DELTA_V >= -V else -V
                self.vx = 0
            if keys[pygame.K_LEFT]:
                self.cur_frame = 1
                self.vx = self.vx - DELTA_V if self.vx - DELTA_V >= -V else -V
                self.vy = 0
            if keys[pygame.K_RIGHT]:
                self.cur_frame = 2
                self.vx = self.vx + DELTA_V if self.vx + DELTA_V <= V else V
                self.vy = 0
            if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
                self.cur_frame = 4
                self.vx, self.vy = V, -V
            if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
                self.cur_frame = 5
                self.vx, self.vy = V, V
            if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
                self.cur_frame = 7
                self.vx, self.vy = -V, -V
            if keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
                self.cur_frame = 6
                self.vx, self.vy = -V, V
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
        if pygame.sprite.spritecollideany(self, star_group):
            a = pygame.sprite.spritecollide(self, star_group, False)
            for i in a:
                if pygame.sprite.collide_mask(self, i):
                    self.vx = -self.vx
                    self.vy = -self.vy
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(self.vx, self.vy)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
floor_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()
planet_group = pygame.sprite.Group()

player_image = load_image("car2.png")
tile_images = {"sun": load_image("sun.png"), "planet": load_image("planet.png"),
               'wall': [load_image('obstacle.png'), load_image('obstacle2.png'), load_image('obstacle3.png')],
               'empty': load_image('floor.png')}
player, level_x, level_y = generate_level(load_level('aaa.txt'))
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
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
            running = False
    floor_group.draw(screen)
    star_group.draw(screen)
    planet_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(50)

pygame.quit()
