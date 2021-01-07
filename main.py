import math
import pygame
import pygame.freetype
import random
import traceback
import os
import sys
import time

pygame.init()

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
V_45 = 15
STATUS_FONT = pygame.freetype.Font("D3Digitalism.ttf", 24)
NUM_FONT = pygame.freetype.Font("D3Digitalism.ttf", 36)


def load_level(filename):
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_map(filename):
    try:
        with open(filename, 'w') as mapFile:
            a = [["." for i in range(80)] for j in range(80)]
            a[39][39] = "S"
            planets = []
            x1, y1 = random.randint(4, 75), random.randint(4, 75)
            while True:
                if abs(x1 - 39) >= 4 and abs(y1 - 39) >= 4:
                    a[y1][x1] = "P"
                    planets.append([x1, y1])
                    break
                else:
                    x1, y1 = random.randint(4, 75), random.randint(4, 75)

            x1, y1 = random.randint(4, 75), random.randint(4, 75)
            for i in range(random.randint(1, 10)):
                while True:
                    counts = [abs(j[0] - x1) >= 3 and abs(j[1] - y1) >= 3 for j in planets]

                    if abs(x1 - 39) >= 4 and abs(y1 - 39) >= 4 and counts.count(True) == len(counts):
                        a[y1][x1] = "P"
                        planets.append([x1, y1])
                        break
                    else:
                        x1, y1 = random.randint(4, 75), random.randint(4, 75)

            a[24][24] = "@"

            a = "".join(["".join(i) + "\n" for i in a])
            mapFile.write(a)
    except Exception:
        print(traceback.format_exc())


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


class Scan(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, frame, columns=8, rows=1):
        super().__init__(scan_group, all_sprites)
        self.frames = []
        self.cur_frame = frame
        self.cut_sheet(tile_images["scan"], columns, rows)
        self.image = self.frames[self.cur_frame]
        self.image.convert_alpha()
        self.rect = self.rect.move(pos_x, pos_y)
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
        self.image = random.choice(tile_images["planet"])
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


class Status:
    def __init__(self):
        self.surface, self.rect = STATUS_FONT.render("", (0, 0, 0))
        self.to_blit = {
            "success": [STATUS_FONT.render("", (0, 0, 0))[0], (0, 0)],
            "num_known": [STATUS_FONT.render("", (0, 0, 0))[0], (0, 0)]}

    def update(self, text):
        if scan_group.sprites() and text == "success":
            if pygame.sprite.spritecollideany(scan_group.sprites()[0], planet_group):
                a = pygame.sprite.spritecollide(scan_group.sprites()[0], planet_group, False)
                if a[0] not in known:
                    known.append(a[0])
                self.to_blit["success"] = [STATUS_FONT.render("SUCCESS", fgcolor=pygame.Color("red"))[0],
                                           (width // 2 - self.to_blit["success"][0].get_size()[0] // 2, 200)]
                self.to_blit["num_known"] = [NUM_FONT.render(str(len(known)), fgcolor=pygame.Color("red"))[0],
                                             (width - 20 - self.to_blit["num_known"][0].get_size()[0], 20)]
                return True
        return False


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = width // 2
        self.dy = height // 2

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        if not paused:
            obj.rect.x += self.dx
            obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        if not paused:
            self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
            self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, columns=8, rows=1):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.cur_frame = 3
        self.cut_sheet(player_image, columns, rows)
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(pos_x * tile_width, pos_y * tile_height)
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
        global scan_group
        if not paused:
            scan_group = pygame.sprite.Group()
            if keys[pygame.K_DOWN] or keys[pygame.K_UP] or keys[pygame.K_s] or keys[pygame.K_w]:
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.cur_frame = 0
                    self.vy = self.vy + DELTA_V if self.vy + DELTA_V <= V else V
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.cur_frame = 3
                    self.vy = self.vy - DELTA_V if self.vy - DELTA_V >= -V else -V
            else:
                if self.vy > 0:
                    self.vy -= DELTA_V
                    self.vy = 0 if self.vy <= 0 else self.vy
                if self.vy < 0:
                    self.vy += DELTA_V
                    self.vy = 0 if self.vy >= 0 else self.vy

            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_a] or keys[pygame.K_d]:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.cur_frame = 1
                    self.vx = self.vx - DELTA_V if self.vx - DELTA_V >= -V else -V
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.cur_frame = 2
                    self.vx = self.vx + DELTA_V if self.vx + DELTA_V <= V else V
            else:
                if self.vx > 0:
                    self.vx -= DELTA_V
                    self.vx = 0 if self.vx <= 0 else self.vx
                if self.vx < 0:
                    self.vx += DELTA_V
                    self.vx = 0 if self.vx >= 0 else self.vx
            if keys[pygame.K_RIGHT] and keys[pygame.K_UP] or keys[pygame.K_d] and keys[pygame.K_w]:
                self.cur_frame = 4
                # self.vx, self.vy = V_45, -V_45
                scan_group = pygame.sprite.Group()
                scan = True
                # Scan(self.rect.x + tile_height - self.vx, self.rect.y - tile_height + self.vy, 4)
            if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN] or keys[pygame.K_d] and keys[pygame.K_s]:
                self.cur_frame = 5
                # self.vx, self.vy = V_45, V_45
                scan_group = pygame.sprite.Group()
                scan = True
                # Scan(self.rect.x + tile_height - self.vx, self.rect.y + tile_height - self.vy, 5)
            if keys[pygame.K_LEFT] and keys[pygame.K_UP] or keys[pygame.K_a] and keys[pygame.K_w]:
                self.cur_frame = 7
                # self.vx, self.vy = -V_45, -V_45
                scan_group = pygame.sprite.Group()
                scan = True
                # Scan(self.rect.x - tile_height + self.vx, self.rect.y - tile_width + self.vy, 7)
            if keys[pygame.K_LEFT] and keys[pygame.K_DOWN] or keys[pygame.K_a] and keys[pygame.K_s]:
                self.cur_frame = 6
                # self.vx, self.vy = -V_45, V_45
                scan_group = pygame.sprite.Group()
                scan = True
                # Scan(self.rect.x - tile_height - 5, self.rect.y + tile_height + 5, 6)

            """
            if keys[pygame.K_DOWN] or keys[pygame.K_UP] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[
                pygame.K_s] or keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_d]:
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.cur_frame = 0
                    self.vy = self.vy + DELTA_V if self.vy + DELTA_V <= V else V
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.cur_frame = 3
                    self.vy = self.vy - DELTA_V if self.vy - DELTA_V >= -V else -V
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.cur_frame = 1
                    self.vx = self.vx - DELTA_V if self.vx - DELTA_V >= -V else -V
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.cur_frame = 2
                    self.vx = self.vx + DELTA_V if self.vx + DELTA_V <= V else V
                if keys[pygame.K_RIGHT] and keys[pygame.K_UP] or keys[pygame.K_d] and keys[pygame.K_w]:
                    self.cur_frame = 4
                    # self.vx, self.vy = V_45, -V_45
                    scan_group = pygame.sprite.Group()
                    Scan(self.rect.x + tile_height + 5, self.rect.y - tile_height - 5, 4)
                if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN] or keys[pygame.K_d] and keys[pygame.K_s]:
                    self.cur_frame = 5
                    # self.vx, self.vy = V_45, V_45
                    scan_group = pygame.sprite.Group()
                    Scan(self.rect.x + tile_height + 5, self.rect.y + tile_height + 5, 5)
                if keys[pygame.K_LEFT] and keys[pygame.K_UP] or keys[pygame.K_a] and keys[pygame.K_w]:
                    self.cur_frame = 7
                    # self.vx, self.vy = -V_45, -V_45
                    scan_group = pygame.sprite.Group()
                    Scan(self.rect.x - tile_height - 5, self.rect.y - tile_width - 5, 7)
                if keys[pygame.K_LEFT] and keys[pygame.K_DOWN] or keys[pygame.K_a] and keys[pygame.K_s]:
                    self.cur_frame = 6
                    # self.vx, self.vy = -V_45, V_45
                    scan_group = pygame.sprite.Group()
                    Scan(self.rect.x - tile_height - 5, self.rect.y + tile_height + 5, 6)
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
            """
            if pygame.sprite.spritecollideany(self, star_group) or pygame.sprite.spritecollideany(self, planet_group):
                a = pygame.sprite.spritecollide(self, star_group, False)
                b = pygame.sprite.spritecollide(self, planet_group, False)

                for i in a:
                    if pygame.sprite.collide_mask(self, i):
                        self.vx = -self.vx
                        self.vy = -self.vy

                for i in b:
                    if pygame.sprite.collide_mask(self, i):
                        self.vx = -self.vx
                        self.vy = -self.vy
            self.image = self.frames[self.cur_frame]

            self.rect = self.rect.move(self.vx, self.vy)
            if keys[pygame.K_SPACE]:
                if self.cur_frame == 0:
                    scan_group = pygame.sprite.Group()
                    Scan(self.rect.x, self.rect.y + tile_height, 2)
                if self.cur_frame == 1:
                    scan_group = pygame.sprite.Group()
                    Scan(self.rect.x - tile_width, self.rect.y, 3)
                if self.cur_frame == 2:
                    scan_group = pygame.sprite.Group()
                    Scan(self.rect.x + tile_width, self.rect.y, 1)
                if self.cur_frame == 3:
                    scan_group = pygame.sprite.Group()
                    Scan(self.rect.x, self.rect.y - tile_height, 0)
                if self.cur_frame == 4:
                    scan_group = pygame.sprite.Group()
                    Scan(self.rect.x + tile_width - 7, self.rect.y - tile_height + 7, 4)
                if self.cur_frame == 5:
                    scan_group = pygame.sprite.Group()
                    Scan(self.rect.x + tile_width - 7, self.rect.y + tile_height - 7, 5)
                if self.cur_frame == 6:
                    scan_group = pygame.sprite.Group()
                    Scan(self.rect.x - tile_width + 7, self.rect.y + tile_height - 7, 6)
                if self.cur_frame == 7:
                    scan_group = pygame.sprite.Group()
                    Scan(self.rect.x - tile_width + 7, self.rect.y - tile_height + 7, 7)
            else:
                scan_group = pygame.sprite.Group()


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
floor_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()
planet_group = pygame.sprite.Group()
scan_group = pygame.sprite.Group()
player_image = load_image("car2.png")
tile_images = {"sun": load_image("sun.png"),
               "planet": [load_image("planet.png"), load_image("planet2.png"), load_image("planet3.png")],
               'wall': [load_image('obstacle.png'), load_image('obstacle2.png'), load_image('obstacle3.png')],
               'empty': load_image('floor.png'), "scan": load_image("scan.png"), "success": load_image("success.png")}

player, level_x, level_y = generate_level(load_level('sport.txt'))
camera = Camera()
status = Status()
known = []
paused = False
start = time.time()
printed_time = False
while running:
    key = pygame.key.get_pressed()
    if key[pygame.K_p]:
        if not paused:
            paused = True

        else:
            paused = False
    screen.fill(pygame.Color('black'))
    player_group.update(key)
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
            running = False

    floor_group.draw(screen)
    star_group.draw(screen)
    planet_group.draw(screen)
    player_group.draw(screen)
    scan_group.draw(screen)
    if status.update("success"):
        screen.blit(*status.to_blit["success"])
    screen.blit(*status.to_blit["num_known"])
    if len(known) == len(planet_group.sprites()):
        if not printed_time:
            end = time.time()
        screen.blit(NUM_FONT.render(str(round(end - start, 2)), fgcolor=pygame.Color("red"))[0], (20, 20))
        printed_time = True
    pygame.display.flip()
    clock.tick(50)

pygame.quit()
