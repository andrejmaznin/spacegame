import math
import pygame
import pygame.freetype
import random
import traceback
import os
import sys
import time
# import simpleaudio
from random import randint

pygame.init()

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
BIG_FONT = pygame.freetype.Font("D3Digitalism.ttf", 46)

TEXT_FONT = pygame.freetype.Font("Tomba2Full.ttf", 36)
tiles_x, tiles_y = 0, 0
MAPS = ['map_0.txt', 'map_1.txt', 'map_2.txt', 'map_3.txt']


def restart():
    global player, level_x, level_y, camera, status, known, paused, start, printed_time, button_exit, button_restart, \
        button_pause, top_right, bottom_left, asteroid_group, atmosphere_group, _cycle_, system_Number, planets
    new_groups()
    planets = {}
    known = 0
    for el in MAPS:
        generate_map("maps/" + el)
    player, level_x, level_y = generate_level(load_level("maps/" + 'map_1.txt'))
    camera = Camera()
    status = Status()
    paused = False
    start = time.time()
    printed_time = False
    bottom_left = floor_group.sprites()[-1]
    top_right = floor_group.sprites()[0]
    _cycle_ = 'Main Cycle'
    system_Number = 1


def new_groups():
    global all_sprites, tiles_group, player_group, floor_group, star_group, planet_group, \
        scan_group, atmosphere_group, asteroid_group

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    floor_group = pygame.sprite.Group()
    star_group = pygame.sprite.Group()
    planet_group = pygame.sprite.Group()
    scan_group = pygame.sprite.Group()
    atmosphere_group = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    if "saved_planets" in level_map[0].lower():
        max_width = max(map(len, level_map[2:]))

        return level_map[:2] + list(map(lambda x: x.ljust(max_width, '.'), level_map[2:]))
    elif level_map[0].lower() == "saved":
        max_width = max(map(len, level_map[1:]))
        return level_map[:1] + list(map(lambda x: x.ljust(max_width, '.'), level_map[1:]))

    else:
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def clear():
    for filename in MAPS:
        with open("maps/" + filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
            if level_map[0] == "saved":
                level_map = level_map[1:]

        level_map = "".join(["".join(i) + "\n" for i in level_map])

        with open("maps/" + filename, 'w') as mapFile:
            # print(level_map)
            # print(type(level_map))
            mapFile.write(level_map)
            mapFile.close()


def save_planets(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

        if "saved" in level_map[0].lower():
            level_map[0] = "saved_planets"
            level_map[1] = str(planets)

            if systems[cur_system]:
                level_map[2] = f"{start} {end}"

            else:
                level_map[2] = f"-1 -1"
        else:
            if systems[cur_system]:
                level_map.insert(0, f"{start} {end}")

            else:
                level_map.insert(0, f"-1 -1")
            level_map.insert(0, str(planets))
            level_map.insert(0, "saved_planets")

    level_map = "".join(["".join(i) + "\n" for i in level_map])
    with open(filename, 'w') as mapFile:
        # print(level_map)
        # print(type(level_map))
        mapFile.write(level_map)
        mapFile.close()


def save_done(filename):
    filename = "maps/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        if "saved" not in level_map[0].lower():
            level_map.insert(0, "saved")

    level_map = "".join(["".join(i) + "\n" for i in level_map])

    with open(filename, 'w') as mapFile:
        # print(level_map)
        # print(type(level_map))
        mapFile.write(level_map)
        mapFile.close()


def save(filename):
    x_f, y_f = floor_group.sprites()[0].rect.x, floor_group.sprites()[0].rect.y
    x_p, y_p = player.rect.x, player.rect.y
    x, y = abs(x_f - x_p), abs(y_f - y_p)
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

        if "saved" in level_map[0].lower():
            level_map[0] = "saved"
            level_map[1] = str(x) + " " + str(y)
            level_map[2] = str(known)
            level_map[3] = "system_name"
            level_map[4] = str(planets)

        else:
            level_map.insert(0, str(planets))
            level_map.insert(0, "system_name")
            level_map.insert(0, str(known))
            level_map.insert(0, str(x) + " " + str(y))
            level_map.insert(0, "saved")

        level_map = "".join(["".join(i) + "\n" for i in level_map])
        mapFile.close()
    with open(filename, 'w') as mapFile:
        # print(level_map)
        # print(type(level_map))
        mapFile.write(level_map)
        mapFile.close()

    # сохранение настроек
    with open('info.txt', 'w') as infoFile:
        global volume
        # print(str(round(volume, 2)))
        print(str(round(volume, 2)), file=infoFile)


def load_settings():
    with open('info.txt', 'r') as infoFile:
        global volume
        settings = infoFile.read().strip().split('\n')
        volume = round(float(settings[0]), 2)


def generate_map(filename):
    try:
        with open(filename, 'w') as mapFile:
            a = [["." for i in range(50)] for j in range(50)]
            a[24][24] = "S"
            planets = []
            x1, y1 = random.randint(4, 45), random.randint(4, 45)
            while True:
                if abs(x1 - 24) >= 5 and abs(y1 - 24) >= 5:
                    a[y1][x1] = str(random.randint(0, 2))
                    planets.append([x1, y1])
                    break

                else:
                    x1, y1 = random.randint(4, 45), random.randint(4, 45)

            x1, y1 = random.randint(4, 45), random.randint(4, 45)
            for i in range(random.randint(1, 6)):
                while True:
                    counts = [abs(j[0] - x1) >= 3 and abs(j[1] - y1) >= 3 for j in planets]

                    if abs(x1 - 24) >= 4 and abs(y1 - 24) >= 4 and counts.count(True) == len(counts):
                        a[y1][x1] = str(random.randint(0, 2))
                        planets.append([x1, y1])
                        break

                    else:
                        x1, y1 = random.randint(4, 45), random.randint(4, 45)

            a[23][23] = "@"
            a[22][22] = "A"
            a = "".join(["".join(i) + "\n" for i in a])
            mapFile.write(a)

    except Exception:
        print(traceback.format_exc())


def generate_level(level, start=False, name=""):
    global tiles_x, tiles_y, known, planets, load
    if not start:
        if "saved_planets" in level[0].lower():
            lev = level[2:]
            planets = eval(level[1])
            new = False
            new_player, x, y = None, None, None

        else:
            new = True
            new_player, x, y = None, None, None
            lev = level

    elif level[0].lower() == "saved":
        lev = level[1:]
        systems[name] = True
        new = False
        load = True
        new_player, x, y = None, None, None

    else:
        new = True
        load = False
        new_player, x, y = None, None, None
        lev = level

    tiles_y = len(lev)
    tiles_x = len(lev[0])
    p_count = 0

    for y in range(50):
        for x in range(len(lev[y])):
            if lev[y][x] == 'S':
                Floor(x, y)
                Star(x, y)

            elif lev[y][x] == ".":
                Floor(x, y)

            elif lev[y][x].isdigit():
                Floor(x, y)
                if new:
                    planets[f"{x}, {y}"] = [str(p_count), "unknown"]
                    p_count += 1
                else:
                    if planets[f"{x}, {y}"][1] == "known":
                        known += 1
                Planet(x, y, int(lev[y][x]))

            elif lev[y][x] == 'A':
                Floor(x, y)
                Asteroid(x, y)

            elif lev[y][x] == '@':
                Floor(x, y)

                if not new_player:
                    new_player = Player(tile_width * x, tile_height * y)

    return new_player, x, y


def load_image(name, colorkey=None):
    # ���� ���� �� ����������, �� �������
    if not os.path.isfile(name):
        # print(f"���� � ������������ '{name}' �� ������")
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


def minimap():
    x_f, y_f = floor_group.sprites()[0].rect.x, floor_group.sprites()[0].rect.y
    x_p, y_p = player.rect.x, player.rect.y
    mini_width = tile_width * 2 // tiles_x
    mini_height = tile_height * 2 // tiles_y
    sc = pygame.surface.Surface((200, 200))
    x, y = abs((x_f - x_p) // 100), abs((y_f - y_p) // 100)
    if pygame.sprite.spritecollideany(player, floor_group):
        pygame.draw.rect(sc, (255, 255, 255), (x * 4, y * 4, 4, 4))
    pygame.draw.rect(sc, (255, 255, 255), (0, 0, 200, 200), 1)
    screen.blit(sc, (0, height - 200))


def start_game():
    global _cycle_
    _cycle_ = 'Main Cycle'


def show_settings():
    global _cycle_, menu
    if _cycle_ == "Start Menu":
        SETTINGS_MENU.set_k_escape_function(return_to_main_menu)
    elif _cycle_ == "Pause":
        SETTINGS_MENU.set_k_escape_function(set_pause)
    _cycle_ = 'Settings'


def return_to_main_menu():
    global _cycle_, MAPS, system_Number
    _cycle_ = 'Start Menu'


def show_star_system_map():
    global _cycle_
    _cycle_ = "Star System Map"


def continue_game():
    global _cycle_
    _cycle_ = 'Main Cycle'


def do_nothing():
    pass


def decrease_vol():
    global volume, scan_sound
    volume = (volume - 0.01) % 1
    pygame.mixer.music.set_volume(volume)
    scan_sound.set_volume(volume)


def increase_vol():
    global volume
    volume = (volume + 0.01) % 1
    pygame.mixer.music.set_volume(volume)
    scan_sound.set_volume(volume)


def set_pause():
    global _cycle_
    _cycle_ = 'Pause'


def change_star_system():
    global system_Number, _cycle_, player, level_x, level_y, MAPS, camera, status, bottom_left, top_right, known, planets, t, t1, printed_time, cur_system, start, end
    known = 0
    save_done(MAPS[system_Number])
    planets = {}
    new_groups()
    t, t1, start, end = 0, 0, time.time(), 0
    printed_time = False
    system_Number = STAR_MAP.planet_number()
    cur_system = MAPS[system_Number]
    player, level_x, level_y = generate_level(load_level("maps/" + MAPS[system_Number]), name=MAPS[system_Number])
    camera = Camera()
    status = Status()
    bottom_left = floor_group.sprites()[-1]
    top_right = floor_group.sprites()[0]
    _cycle_ = 'Main Cycle'


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
    def __init__(self, pos_x, pos_y, img):
        super().__init__(planet_group, all_sprites)
        self.image = tile_images["planet"][img]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.center = (self.rect.x + tile_width, self.rect.y + tile_height)
        self.mask = pygame.mask.from_surface(self.image)
        Atmosphere(pos_x, pos_y, img)

    def update(self):
        self.center = (self.rect.x + self.rect.size[0] // 2, self.rect.y + self.rect.size[1] // 2)


def inertion(cur, min, delta):
    if cur > 0:
        cur -= delta
        cur = min if cur <= min else cur
    if cur < 0:
        cur += delta
        cur = -min if cur > -min else cur
    return int(cur)


class Atmosphere(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, num):
        super().__init__(atmosphere_group, all_sprites)
        self.x, self.y = pos_x, pos_y
        self.image = tile_images["atmosphere"][num]
        self.rect = self.image.get_rect().move(
            tile_width * (pos_x - 1), tile_height * (pos_y - 1))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if pygame.sprite.spritecollideany(player, atmosphere_group):
            a = pygame.sprite.spritecollide(player, atmosphere_group, False)
            if pygame.sprite.collide_mask(a[0], player):
                vx = inertion(player.vx, 0, 0.5) if player.vx else 0
                vy = inertion(player.vx, 0, 0.5) if player.vy else 0
                player.vx, player.vy = vx, vy


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
            "num_known": [NUM_FONT.render(str(known) + "/" + str(len(planets.keys())), fgcolor=pygame.Color("red"))[0],
                          (width - 20 - NUM_FONT.render(str(known) + "/" + str(len(planets.keys())))[0].get_size()[0],
                           20)],
            "restart": [STATUS_FONT.render("", (0, 0, 0))[0], (0, 0)],
            "explored": [BIG_FONT.render("EXPLORED", fgcolor=pygame.Color("blue"))[0],
                         (width // 2 - BIG_FONT.render("EXPLORED")[0].get_size()[0] // 2, 120)]}

    def update(self, text):
        global known
        if scan_group.sprites() and text == "success":
            if pygame.sprite.spritecollideany(scan_group.sprites()[0], atmosphere_group):
                a = pygame.sprite.spritecollide(scan_group.sprites()[0], atmosphere_group, False)
                x, y = a[0].x, a[0].y
                if planets[f"{x}, {y}"][1] == "unknown":
                    known += 1
                    planets[f"{x}, {y}"][1] = "known"

                self.to_blit["success"] = [STATUS_FONT.render("SUCCESS", fgcolor=pygame.Color("red"))[0],
                                           (width // 2 - self.to_blit["success"][0].get_size()[0] // 2, 200)]
                self.to_blit["num_known"] = [
                    NUM_FONT.render(str(known) + "/" + str(len(planets.keys())), fgcolor=pygame.Color("red"))[0],
                    (width - 20 - NUM_FONT.render(str(known) + "/" + str(len(planets.keys())))[0].get_size()[0], 20)]
                return True

        return False


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        # if bottom_left.rect.y - player.rect.y >= height // 2 <= player.rect.y - top_right.rect.y:
        if not self.stop_y:
            obj.rect.y += self.dy

        # if bottom_left.rect.x - player.rect.x >= width // 2 <= player.rect.x - top_right.rect.x:
        if not self.stop_x:
            obj.rect.x += self.dx

    # позиционировать камеру на объекте target
    def update(self, target):
        if player.rect.x - top_right.rect.x > width // 2 < bottom_left.rect.x - player.rect.x:
            self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
            self.stop_x = False
        else:
            self.stop_x = True
        if player.rect.y - top_right.rect.y > height // 2 < bottom_left.rect.y - player.rect.y:
            self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
            self.stop_y = False
        else:
            self.stop_y = True

        # self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
        # self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)


def move(obj, cur, side):
    if obj == "player":
        if side:
            return cur + DELTA_V if cur + DELTA_V <= V else V
        return cur - DELTA_V if cur - DELTA_V >= -V else -V


def check_frames(keys, default):
    cur_frame = default
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        cur_frame = 0
    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        cur_frame = 3
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        cur_frame = 1
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        cur_frame = 2
    if keys[pygame.K_RIGHT] and keys[pygame.K_UP] or keys[pygame.K_d] and keys[pygame.K_w]:
        cur_frame = 4
    if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN] or keys[pygame.K_d] and keys[pygame.K_s]:
        cur_frame = 5
    if keys[pygame.K_LEFT] and keys[pygame.K_UP] or keys[pygame.K_a] and keys[pygame.K_w]:
        cur_frame = 7
    if keys[pygame.K_LEFT] and keys[pygame.K_DOWN] or keys[pygame.K_a] and keys[pygame.K_s]:
        cur_frame = 6

    return cur_frame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, columns=8, rows=1):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.cur_frame = 3
        self.cut_sheet(player_image, columns, rows)
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(pos_x, pos_y)
        self.center = [self.rect.x + tile_width // 2, self.rect.y + tile_height // 2]
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
        global scan_group, scan_sound
        self.center = [self.rect.x + tile_width // 2, self.rect.y + tile_height // 2]
        if not paused:
            scan_group = pygame.sprite.Group()
            if keys[pygame.K_DOWN] or keys[pygame.K_UP] or keys[pygame.K_s] or keys[pygame.K_w]:
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    side = True
                elif keys[pygame.K_UP] or keys[pygame.K_w]:
                    side = False
                self.vy = move("player", self.vy, side)
            else:
                self.vy = inertion(self.vy, 0, DELTA_V)

            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_a] or keys[pygame.K_d]:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    side = False
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    side = True
                self.vx = move("player", self.vx, side)
            else:
                self.vx = inertion(self.vx, 0, DELTA_V)
            self.cur_frame = check_frames(keys, self.cur_frame)

            if pygame.sprite.spritecollideany(self, star_group) or pygame.sprite.spritecollideany(self, planet_group):
                a = pygame.sprite.spritecollide(self, star_group, False)
                b = pygame.sprite.spritecollide(self, planet_group, False)

                for i in a:
                    if pygame.sprite.collide_mask(self, i):
                        self.vx = -self.vx
                        self.vy = -self.vy

                for i in b:
                    if pygame.sprite.collide_mask(self, i):
                        if (self.center[0] - i.center[0]) * self.vx < 0:
                            self.vx = -self.vx
                        if (self.center[1] - i.center[1]) * self.vy < 0:
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


class Message:
    def __init__(self, filename):
        with open(filename) as textFile:
            self.surface = pygame.Surface((800, 400))
            text = [i.strip() for i in textFile]
            pygame.draw.rect(self.surface, (255, 255, 255), (0, 0, 800, 400), 4)
            self.text_surfaces = [TEXT_FONT.render(i, (255, 255, 255)) for i in text]
            x, y = 40, 20
            self.surface.blit(self.text_surfaces[0][0], (x, y))
            y += 30
            for i in self.text_surfaces[1:]:
                self.surface.blit(i[0], (x, y))
                y += 30
            self.button, self.button_rect = TEXT_FONT.render("X", (255, 0, 0))
            self.but_x, self.but_y = 800 - 10 - self.button.get_size()[0], 10
            self.surface.blit(self.button, (800 - 10 - self.button.get_size()[0], 10))

    def update(self, pos):
        global show_text
        if self.but_x + 400 <= pos[0] <= self.but_x + self.button.get_size()[0] + 400 and self.but_y + 400 <= pos[
            1] <= self.but_y + 400 + \
                self.button.get_size()[1]:
            show_text = False


class Menu:
    def __init__(self, screen, cycle_name, buttons=[[100, 100, 'exit', (255, 0, 0), (0, 0, 255), sys.exit]],
                 k_escape_fun=sys.exit):
        self.buttons = buttons
        self.screen = screen
        self.k_escape = k_escape_fun
        self.font = pygame.freetype.Font("D3Digitalism.ttf", 50)
        self.cycle_name = cycle_name
        self.stars = []

    def show_buttons(self, btn_num=-1):
        for btn in self.buttons:
            if btn_num == self.buttons.index(btn) and btn_num != -1:
                self.screen.blit(self.font.render(btn[2], btn[4])[0], (btn[0], btn[1]))
            else:
                self.screen.blit(self.font.render(btn[2], btn[3])[0], (btn[0], btn[1]))

    def show_menu(self):
        global _cycle_
        while _cycle_ == self.cycle_name:
            btn = -1
            self.screen.fill((0, 0, 0))

            for el in self.stars:
                pygame.draw.circle(self.screen, (255, 255, 255), (el[0], el[1]), el[2])
            btn = self.check_buttons(btn)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        function = self.k_escape
                        function()
                        break
                if event.type == pygame.MOUSEBUTTONUP:
                    if btn != -1:
                        function = self.buttons[btn][5]
                        function()

            pygame.display.flip()

    def generate_stars(self, num, divider):
        x, y = pygame.display.get_window_size()
        for i in range(num):
            coord_x = randint(int(x / divider), x)
            coord_y = randint(int(y / divider), y)
            raduis = randint(1, 2)
            self.stars.append((coord_x, coord_y, raduis))

    def generate_sky(self):
        self.generate_stars(200, 2)
        self.generate_stars(100, 4)
        self.generate_stars(50, 8)

    def check_buttons(self, btn):
        x, y = pygame.mouse.get_pos()
        for b in self.buttons:
            if x > b[0] and x < b[0] + 41 * len(b[2]) and y > b[1] and y < b[1] + 50:
                btn = self.buttons.index(b)
        self.show_buttons(btn)
        return btn

    def make_btn_return(self):
        x, y = pygame.mouse.get_pos()
        if 25 <= x <= 60 and 25 <= y <= 60:
            pygame.draw.polygon(self.screen, (0, 0, 255), ((60, 25), (60, 60), (25, 43)))
            return True
        pygame.draw.polygon(self.screen, (255, 0, 0), ((60, 25), (60, 60), (25, 43)))
        return False


class SettingsMenu(Menu):
    def __init__(self, screen, cycle_name='Settings',
                 buttons=[[100, 100, 'VOLUME', (255, 0, 0), (255, 0, 255), decrease_vol, increase_vol, (0, 100)]],
                 k_escape_fun=set_pause):
        super().__init__(screen, cycle_name, buttons, k_escape_fun)

    def show_menu(self):
        global _cycle_
        while self.cycle_name == _cycle_:
            self.screen.fill((0, 0, 0))
            return_btn = self.make_btn_return()
            for i in range(len(self.buttons)):
                self.show_button(i)
            btn_num, side = self.check_button()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        function = self.k_escape
                        function()
                        break
                if event.type == pygame.MOUSEBUTTONUP:
                    if return_btn:
                        function = self.k_escape
                        function()
                    if side == 1:
                        function = self.buttons[btn_num][5]
                        function()
                    if side == 2:
                        function = self.buttons[btn_num][6]
                        function()

            pygame.display.flip()

    def show_button(self, btn_num):
        x, y = pygame.display.get_window_size()
        x_mouse, y_mouse = pygame.mouse.get_pos()
        if self.buttons[btn_num][1] + 50 >= y_mouse >= self.buttons[btn_num][1]:
            self.screen.blit(self.font.render(self.buttons[btn_num][2], self.buttons[btn_num][4])[0],
                             (self.buttons[btn_num][0], self.buttons[btn_num][1]))
            self.screen.blit(self.font.render(str(int(volume * 100)), self.buttons[btn_num][4])[0],
                             (x - 233, self.buttons[btn_num][1] + 10))
            if x - 100 >= x_mouse >= x - 120:
                self.draw_pointer((0, 0, 255), x - 120, self.buttons[btn_num][1] + 50, 1)
            else:
                self.draw_pointer((255, 0, 255), x - 120, self.buttons[btn_num][1] + 50, 1)
            if x - 240 >= x_mouse > x - 260:
                self.draw_pointer((0, 0, 255), x - 260, self.buttons[btn_num][1] + 50, 2)
            else:
                self.draw_pointer((255, 0, 255), x - 260, self.buttons[btn_num][1] + 50, 2)
        else:
            self.screen.blit(self.font.render(self.buttons[btn_num][2], self.buttons[btn_num][3])[0],
                             (self.buttons[btn_num][0], self.buttons[btn_num][1]))
            self.draw_pointer((255, 0, 0), x - 120, self.buttons[btn_num][1] + 50, 1)
            self.screen.blit(self.font.render(str(int(volume * 100)), self.buttons[btn_num][3])[0],
                             (x - 233, self.buttons[btn_num][1] + 10))
            self.draw_pointer((255, 0, 0), x - 260, self.buttons[btn_num][1] + 50, 2)

    def check_button(self):
        x, y = pygame.display.get_window_size()
        x_mouse, y_mouse = pygame.mouse.get_pos()
        btn, side = -1, -1
        for i in range(len(self.buttons)):
            if self.buttons[i][1] + 50 >= y_mouse >= self.buttons[i][1] and x - 240 >= x_mouse > x - 260:
                btn, side = i, 1
            elif self.buttons[i][1] + 50 >= y_mouse >= self.buttons[i][1] and x - 100 >= x_mouse >= x - 120:
                btn, side = i, 2
        return (btn, side)

    def draw_pointer(self, color, x, y, type):
        if type == 1:
            pygame.draw.polygon(self.screen, color, ((x, y), (x + 20, y - 25), (x, y - 50)), 5)
        elif type == 2:
            pygame.draw.polygon(self.screen, color, ((x, y - 25), (x + 20, y - 50), (x + 20, y)), 5)

    def set_k_escape_function(self, function):
        self.k_escape = function


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, columns=1, rows=1):
        super().__init__(asteroid_group, all_sprites)
        self.frames = []
        self.cur_frame = 0
        self.cut_sheet(tile_images["wall"], columns, rows)
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(pos_x * tile_width, pos_y * tile_height)
        self.center = [self.rect.x + tile_width // 2, self.rect.y + tile_height // 2]
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
        global scan_group, scan_sound
        self.center = [self.rect.x + tile_width // 2, self.rect.y + tile_height // 2]
        if not paused:
            if pygame.sprite.spritecollideany(self, atmosphere_group):
                a = pygame.sprite.spritecollide(self, atmosphere_group, False)
                if pygame.sprite.collide_mask(a[0], player):
                    vx = inertion(self.vx, 0, 1) if self.vx else 0
                    vy = inertion(self.vy, 0, 0.5) if self.vy else 0
                    self.vx, self.vy = vx, vy
            if pygame.sprite.spritecollideany(self, star_group) or pygame.sprite.spritecollideany(self, planet_group):
                a = pygame.sprite.spritecollide(self, star_group, False)
                b = pygame.sprite.spritecollide(self, planet_group, False)

                for i in a:
                    if pygame.sprite.collide_mask(self, i):
                        self.vx = -self.vx
                        self.vy = -self.vy

                for i in b:
                    if pygame.sprite.collide_mask(self, i):
                        if (self.center[0] - i.center[0]) * self.vx < 0:
                            self.vx = -self.vx
                        if (self.center[1] - i.center[1]) * self.vy < 0:
                            self.vy = -self.vy
            if pygame.sprite.spritecollideany(self, player_group):
                x = player.vx
                y = player.vy
                self.vx = self.vx + int(x * 0.5) if abs(self.vx <= V) else self.vx
                self.vy = self.vy + int(y * 0.5) if abs(self.vy <= V) else self.vy
                player.vx = int(x * 0.3)
                player.vy = int(y * 0.3)

            self.image = self.frames[self.cur_frame]
            self.rect = self.rect.move(self.vx, self.vy)


class StarSystemMap(Menu):
    def __init__(self, screen, cycle_name, buttons=[[100, 100, 'exit', (255, 0, 0), (0, 0, 255), sys.exit]],
                 k_escape_fun=sys.exit):
        super().__init__(screen, cycle_name, buttons, k_escape_fun)
        self.planets = [[200, 200, 30, 'PYTHAGORAS'],
                        [400, 400, 30, 'DEMOCRITUS'],
                        [500, 700, 30, 'SOCRATES'],
                        [800, 200, 30, 'ARISTOTLE']]
        self.routes = [(0, 1), (1, 2), (1, 3)]
        self.new_planet = -1

    def show_map(self):
        try:
            global _cycle_
            while self.cycle_name == _cycle_:
                screen.fill((0, 0, 0))
                route, planet = self.check_routes()
                self.show_planets(route, planet)
                btn_return = self.make_btn_return()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_ESCAPE:
                            set_pause()
                            break
                    if event.type == pygame.MOUSEBUTTONUP:
                        if planet != -1:
                            self.new_planet = planet
                            ask_map(self.screen)
                        if btn_return:
                            set_pause()

                pygame.display.flip()
        except Exception:
            print(traceback.format_exc())

    def show_planets(self, route, planet):
        global system_Number
        for el in self.routes:
            if el == route:
                pygame.draw.line(self.screen, (0, 0, 255), (self.planets[el[0]][0], self.planets[el[0]][1]),
                                 (self.planets[el[1]][0], self.planets[el[1]][1]), width=20)
            else:
                pygame.draw.line(self.screen, (255, 0, 0), (self.planets[el[0]][0], self.planets[el[0]][1]),
                                 (self.planets[el[1]][0], self.planets[el[1]][1]), width=15)
        for i in range(len(self.planets)):
            if i == system_Number:
                pygame.draw.circle(self.screen, (255, 255, 255), (self.planets[i][0], self.planets[i][1]),
                                   self.planets[i][2])
                self.screen.blit(self.font.render(self.planets[i][3], (255, 255, 255))[0], (270, 70))
            elif i == planet:
                self.screen.blit(self.font.render(self.planets[i][3], (255, 0, 0))[0], (700, 400))
                pygame.draw.circle(self.screen, (0, 0, 255), (self.planets[i][0], self.planets[i][1]),
                                   self.planets[i][2] + 5)

            else:
                pygame.draw.circle(self.screen, (255, 0, 0), (self.planets[i][0], self.planets[i][1]),
                                   self.planets[i][2])

    def check_routes(self):
        global system_Number
        x, y = pygame.mouse.get_pos()
        main_route = (-1, -1)
        main_planet = -1
        if systems[cur_system]:
            for i in range(len(self.planets)):
                if (self.planets[i][0] - x) ** 2 + (self.planets[i][1] - y) ** 2 <= self.planets[i][2] ** 2:
                    if (min(i, system_Number), max(i, system_Number)) in self.routes:
                        main_route = (min(i, system_Number), max(i, system_Number))
                        main_planet = i
        return (main_route, main_planet)

    def planet_number(self):
        return self.new_planet


def ask_map(screen):
    global _cycle_
    _cycle_ = 'Ask'
    ask = Menu(screen, "Ask", buttons=[[100, 100, "CHANGE STAR SYSTEM?", (255, 255, 255), (255, 255, 255), do_nothing],
                                       [100, 170, "YES", (255, 0, 0,), (0, 0, 255), change_star_system],
                                       [100, 240, "NO", (255, 0, 0), (0, 0, 255), show_star_system_map]],
               k_escape_fun=do_nothing)
    ask.show_menu()


def ask_restart():
    global screen, _cycle_
    _cycle_ = 'Ask'
    ask = Menu(screen, "Ask",
               buttons=[[100, 100, "RESTART GAME PROGRESS?", (255, 255, 255), (255, 255, 255), do_nothing],
                        [100, 170, "YES", (255, 0, 0,), (0, 0, 255), restart],
                        [100, 240, "NO", (255, 0, 0), (0, 0, 255), return_to_main_menu]],
               k_escape_fun=do_nothing)
    ask.show_menu()


_cycle_ = "Start Menu"
system_Number = 1
known = 0
planets = {}
load = False
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
floor_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()
planet_group = pygame.sprite.Group()
scan_group = pygame.sprite.Group()
atmosphere_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
clear()

player_image = load_image("images/car2.png")
tile_images = {"sun": load_image("images/sun.png"),
               "planet": [load_image("images/planet.png"), load_image("images/planet2.png"),
                          load_image("images/planet3.png")],
               'wall': load_image('images/obstacle.png'),
               'empty': load_image('images/floor.png'), "scan": load_image("images/scan.png"),
               "success": load_image("images/success.png"),
               "atmosphere": [load_image("images/atmosphere.png"), load_image("images/atmosphere2.png"),
                              load_image("images/atmosphere3.png")]}
player, level_x, level_y = generate_level(load_level("maps/" + MAPS[system_Number]), start=True)
status = Status()
camera = Camera()
bottom_left = floor_group.sprites()[-1]
top_right = floor_group.sprites()[0]
messages = []
messages.append(Message("text.txt"))
paused = False
start = time.time()
printed_time = False
t = 0
t1 = 0
show_text = False
volume = 0
scan_sound = pygame.mixer.Sound("scan.wav")
pygame.mixer.music.load('moon.mp3')
pygame.mixer.music.play()
load_settings()
print(volume)
pygame.mixer.music.set_volume(volume)
scan_sound.set_volume(volume)
end = 0
a = 0.0
cur_system = MAPS[system_Number]
systems = {}
for i in MAPS:
    systems[i] = False
for i in range(3):
    pygame.mixer.music.queue("moon.mp3")

START_MENU = Menu(screen, 'Start Menu', buttons=[[100, 100, 'USE DEFAULT MAPS', (255, 0, 0), (0, 0, 255), start_game],
                                                 [100, 170, 'GENERATE MAPS', (255, 0, 0), (0, 0, 255), ask_restart],
                                                 [100, 240, 'SETTINGS', (255, 0, 0), (0, 0, 255), show_settings],
                                                 [100, 310, 'EXIT', (255, 0, 0), (0, 0, 255), sys.exit]])

PAUSE_MENU = Menu(screen, "Pause", buttons=[[100, 100, "CONTINUE", (0, 100, 0), (0, 0, 255), continue_game],
                                            [100, 170, "MAIN MENU", (255, 0, 0,), (0, 0, 255), return_to_main_menu],
                                            [100, 240, "STAR SYSTEMS MAP", (255, 0, 0), (0, 0, 255),
                                             show_star_system_map],
                                            [100, 310, "SETTINGS", (255, 0, 0), (0, 0, 255), show_settings]],
                  k_escape_fun=continue_game)
STAR_MAP = StarSystemMap(screen, 'Star System Map', k_escape_fun=do_nothing)
ERROR_SCREEN = Menu(screen, _cycle_,
                    buttons=[[100, 100, 'UNEXPECTED ERROR', (255, 255, 255), (255, 255, 255), do_nothing],
                             [100, 170, 'RETURN TO MAIN MENU', (255, 0, 0), (0, 0, 255),
                              return_to_main_menu]], k_escape_fun=do_nothing)
SETTINGS_MENU = SettingsMenu(screen)
START_MENU.generate_sky()
PAUSE_MENU.generate_sky()

while running:
    if _cycle_ == "Start Menu":
        START_MENU.show_menu()

    elif _cycle_ == "Pause":
        PAUSE_MENU.show_menu()

    elif _cycle_ == "Main Cycle":
        if printed_time:
            t = 0
            t1 = 0

        key = pygame.key.get_pressed()
        screen.fill((5, 5, 5))
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        planet_group.update()
        player_group.update(key)
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    set_pause()
                    break
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                messages[0].update(pos)
        floor_group.draw(screen)
        star_group.draw(screen)
        atmosphere_group.draw(screen)
        atmosphere_group.update()
        planet_group.draw(screen)
        asteroid_group.update(key)
        asteroid_group.draw(screen)
        player_group.draw(screen)
        scan_group.draw(screen)
        if status.update("success"):
            screen.blit(*status.to_blit["success"])
            show_text = False
        if show_text:
            screen.blit(messages[0].surface, (400, 400))
        if len(systems.keys()) == list(systems.values()).count(True):
            txt = BIG_FONT.render("TOTAL TIME", fgcolor=pygame.Color("red"))[0]
            time_final = BIG_FONT.render(str(a), fgcolor=pygame.Color("red"))[0]
            screen.blit(txt, (width // 2 - txt.get_size()[0] // 2, 50))
            screen.blit(time_final, (width // 2 - time_final.get_size()[0] // 2, 90))
        else:
            if len(planet_group.sprites()) == known:
                if not printed_time:
                    end = time.time()
                    final = round(end - start + (t1 - t), 2)
                    a += final
                    systems[cur_system] = True
                time_final = NUM_FONT.render(str(final), fgcolor=pygame.Color("red"))[0]
                screen.blit(time_final, (width // 2 - time_final.get_size()[0] // 2, 50))
                printed_time = True

            if systems[cur_system]:
                screen.blit(*status.to_blit["explored"])
            else:
                screen.blit(*status.to_blit["num_known"])
        minimap()
        pygame.display.flip()
        if key[pygame.K_SPACE] and not paused:
            scan_channel = scan_sound.play(0)

        clock.tick(50)

    elif _cycle_ == "Star System Map":
        STAR_MAP.show_map()

    elif _cycle_ == "Settings":
        SETTINGS_MENU.show_menu()

    else:
        ERROR_SCREEN.show_menu()

pygame.quit()
