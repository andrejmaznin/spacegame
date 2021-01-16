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
TEXT_FONT = pygame.freetype.Font("Tomba2Full.ttf", 36)
tiles_x, tiles_y = 0, 0


def restart():
    global player, level_x, level_y, camera, status, known, paused, start, printed_time, all_sprites, tiles_group, \
        planet_group, player_group, star_group, floor_group, scan_group, button_group, button_exit, button_restart, \
        button_pause, top_right, bottom_left, asteroid_group, atmosphere_group
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    floor_group = pygame.sprite.Group()
    star_group = pygame.sprite.Group()
    planet_group = pygame.sprite.Group()
    scan_group = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    atmosphere_group = pygame.sprite.Group()
    generate_map("aaa.txt")
    player, level_x, level_y = generate_level(load_level('aaa.txt'))
    camera = Camera()
    status = Status()
    known = []
    paused = False
    start = time.time()
    printed_time = False
    bottom_left = floor_group.sprites()[-1]
    top_right = floor_group.sprites()[0]


def load_level(filename):
    # ������ �������, ������ ������� �������� ������
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # � ������������ ������������ �����
    max_width = max(map(len, level_map))

    # ��������� ������ ������ ������� �������� ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def save(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        level_map.insert(0, "system_name")
        level_map.insert(0, str(len(known)))
        level_map.insert(0, str(player.rect.x // tile_width) + " " + str(player.rect.y // tile_height))
        level_map.insert(0, "saved")
        level_map = "".join(["".join(i) + "\n" for i in level_map])
        mapFile.close()
    with open(filename, 'w') as mapFile:
        print(level_map)
        print(type(level_map))
        mapFile.write(level_map)
        mapFile.close()


def generate_map(filename):
    try:
        with open(filename, 'w') as mapFile:
            a = [["." for i in range(50)] for j in range(50)]
            a[24][24] = "S"
            planets = []
            x1, y1 = random.randint(4, 45), random.randint(4, 45)
            while True:
                if abs(x1 - 24) >= 5 and abs(y1 - 24) >= 5:
                    a[y1][x1] = "P"
                    planets.append([x1, y1])
                    break
                else:
                    x1, y1 = random.randint(4, 45), random.randint(4, 45)

            x1, y1 = random.randint(4, 45), random.randint(4, 45)
            for i in range(random.randint(1, 6)):
                while True:
                    counts = [abs(j[0] - x1) >= 3 and abs(j[1] - y1) >= 3 for j in planets]

                    if abs(x1 - 24) >= 4 and abs(y1 - 24) >= 4 and counts.count(True) == len(counts):
                        a[y1][x1] = "P"
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


def generate_level(level):
    global tiles_x, tiles_y, known
    if level[0] == "saved":
        new_player = Player(*list(map(int, level[1].split())))
        known = int(level[2])
    else:
        new_player, x, y = None, None, None
    tiles_y = len(level)
    tiles_x = len(level[0])
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
            elif level[y][x] == 'A':
                Floor(x, y)
                Asteroid(x, y)
            elif level[y][x] == '@':
                Floor(x, y)
                if not new_player:
                    new_player = Player(x, y)
    return new_player, x, y


def load_image(name, colorkey=None):
    # ���� ���� �� ����������, �� �������
    if not os.path.isfile(name):
        print(f"���� � ������������ '{name}' �� ������")
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
    x_p, y_p = player.rect.x, player.rect.x
    mini_width = tile_width * 2 // tiles_x
    mini_height = tile_height * 2 // tiles_y
    x, y = int((x_p - x_f)) // tile_width * 4, int((y_p - y_f) // tile_height * 4)
    pygame.draw.rect(screen, (0, 0, 0),
                     (0, height - tile_height * 2, tile_width * 2, tile_height * 2))
    pygame.draw.rect(screen, (255, 255, 255),
                     (0, height - tile_height * 2 - 2, tile_width * 2, tile_height * 2), 2)
    if pygame.sprite.spritecollideany(player, floor_group):
        pygame.draw.rect(screen, (255, 255, 255),
                         (x, height - tile_height * 2 + y, 10, 10))


def start_game():
    global _cycle_
    _cycle_ = 'Main Cycle'
    print(_cycle_)


def show_settings():
    pass


def return_to_main_menu():
    global _cycle_
    save('aaa.txt')
    _cycle_ = 'Start Menu'


def show_star_system_map():
    global _cycle_
    _cycle_ = "Star System Map"


def continue_game():
    global _cycle_
    _cycle_ = 'Main Cycle'


def do_nothing():
    pass


def change_volume(new):
    global volume
    volume = new


def set_pause():
    global _cycle_
    _cycle_ = 'Pause'


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
        num = random.randint(0, len((tile_images["planet"])) - 1)
        self.image = tile_images["planet"][num]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.center = (self.rect.x + tile_width, self.rect.y + tile_height)
        self.mask = pygame.mask.from_surface(self.image)
        Atmosphere(pos_x, pos_y, num)


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
            "num_known": [STATUS_FONT.render("", (0, 0, 0))[0], (0, 0)],
            "restart": [STATUS_FONT.render("", (0, 0, 0))[0], (0, 0)]}

    def update(self, text):
        if scan_group.sprites() and text == "success":
            if pygame.sprite.spritecollideany(scan_group.sprites()[0], atmosphere_group):
                a = pygame.sprite.spritecollide(scan_group.sprites()[0], atmosphere_group, False)

                if a[0] not in known:
                    known.append(a[0])
                self.to_blit["success"] = [STATUS_FONT.render("SUCCESS", fgcolor=pygame.Color("red"))[0],
                                           (width // 2 - self.to_blit["success"][0].get_size()[0] // 2, 200)]
                self.to_blit["num_known"] = [NUM_FONT.render(str(len(known)), fgcolor=pygame.Color("red"))[0],
                                             (width - 20 - self.to_blit["num_known"][0].get_size()[0], 20)]
                return True
        return False


class Camera:
    def __init__(self):
        self.dx = width // 2
        self.dy = height // 2

    def apply(self, obj):
        if not paused:
            if bottom_left.rect.y - player.rect.y >= height // 2 <= player.rect.y - top_right.rect.y:
                obj.rect.y += self.dy
            if bottom_left.rect.x - player.rect.x >= width // 2 <= player.rect.x - top_right.rect.x:
                obj.rect.x += self.dx
        obj.center = (obj.rect.x + tile_width, obj.rect.y + tile_height)

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
                    self.cur_frame = 0
                    self.vy = self.vy + DELTA_V if self.vy + DELTA_V <= V else V
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.cur_frame = 3
                    self.vy = self.vy - DELTA_V if self.vy - DELTA_V >= -V else -V
            else:
                self.vy = inertion(self.vy, 0, DELTA_V)

            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_a] or keys[pygame.K_d]:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.cur_frame = 1
                    self.vx = self.vx - DELTA_V if self.vx - DELTA_V >= -V else -V
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.cur_frame = 2
                    self.vx = self.vx + DELTA_V if self.vx + DELTA_V <= V else V
            else:
                self.vx = inertion(self.vx, 0, DELTA_V)

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


# class SettingsMenu(Menu):
#     def __init__(self, screen, cycle_name='settings',
#                  buttons=[[100, 100, 'VOLUME', (255, 0, 0), (0, 0, 255), change_volume, (0, 100)]],
#                  k_escape_fun=set_pause):
#         super().__init__(self, screen, cycle_name, buttons, k_escape_fun)
#
#     def show_buttons(self, btn_num=-1):
#         for btn in self.buttons:
#             if btn_num == self.buttons.index(btn) and btn_num != -1:
#                 self.screen.blit(self.font.render(btn[2], btn[4])[0], (btn[0], btn[1]))
#             else:
#                 self.screen.blit(self.font.render(btn[2], btn[3])[0], (btn[0], btn[1]))


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
                    vx = inertion(player.vx, 0, 0.5) if self.vx else 0
                    vy = inertion(player.vx, 0, 0.5) if self.vy else 0
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
                print(1)
                x = player.vx
                y = player.vy
                self.vx = self.vx + int(x * 0.5) if abs(self.vx <= V) else self.vx
                self.vy = self.vy + int(y * 0.5) if abs(self.vy <= V) else self.vy
                player.vx = int(x * 0.3)
                player.vy = int(y * 0.3)
            self.image = self.frames[self.cur_frame]
            self.rect = self.rect.move(self.vx, self.vy)


class StarSystemMap:
    def __init__(self, screen):
        self.screen = screen
        self.planets = [[200, 200, 30, 'DIE_1'],
                        [400, 400, 30, 'DIE_2'],
                        [500, 700, 30, 'DIE_3'],
                        [800, 200, 30, 'DIE_4']]
        self.routes = [(0, 1), (1, 2), (1, 3), (2, 1)]
        self.cycle = 'Star System Map'

    def show_map(self):
        global _cycle_
        while self.cycle == _cycle_:
            screen.fill((0, 0, 0))
            self.show_planets()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        set_pause()
                        break

            pygame.display.flip()

    def show_planets(self):
        # route, planet =  self.check_routes()
        for el in self.routes:
            pygame.draw.line(self.screen, (255, 0, 0), (self.planets[el[0]][0], self.planets[el[0]][1]),
                             (self.planets[el[1]][0], self.planets[el[1]][1]), width=15)
        for el in self.planets:
            pygame.draw.circle(self.screen, (255, 0, 0), (el[0], el[1]), el[2])

    # def check_routes(self):
    #     global sytem_Number
    #     x, y = pygame.mouse.get_pos()
    #     for i in range(len(self.planets)):
    #         if (self.planets[i][0] - x) ** 2 + (self.planets[i][1] - y) ** 2 <= self.planets[i][2] ** 2:
    #             if



_cycle_ = "Start Menu"

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
floor_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()
planet_group = pygame.sprite.Group()
scan_group = pygame.sprite.Group()
atmosphere_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
player_image = load_image("car2.png")
tile_images = {"sun": load_image("sun.png"),
               "planet": [load_image("planet.png"), load_image("planet2.png"),
                          load_image("planet3.png")],
               'wall': load_image('obstacle.png'),
               'empty': load_image('floor.png'), "scan": load_image("scan.png"), "success": load_image("success.png"),
               "atmosphere": [load_image("atmosphere.png"), load_image("atmosphere2.png"),
                              load_image("atmosphere3.png")]}
generate_map("aaa.txt")
player, level_x, level_y = generate_level(load_level('aaa.txt'))
camera = Camera()
status = Status()
bottom_left = floor_group.sprites()[-1]
top_right = floor_group.sprites()[0]
messages = []
messages.append(Message("text.txt"))
known = []
paused = False
start = time.time()
printed_time = False
t = 0
t1 = 0
show_text = False
save("aaa.txt")
volume = 100
sytem_Number = 0
scan_sound = pygame.mixer.Sound("scan.wav")
pygame.mixer.music.load('moon.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(volume)
while running:
    if _cycle_ == "Start Menu":
        menu = Menu(screen, 'Start Menu', buttons=[[100, 100, 'START GAME', (255, 0, 0), (0, 0, 255), start_game],
                                                   [100, 170, 'NEW GAME', (255, 0, 0), (0, 0, 255), restart],
                                                   [100, 240, 'SETTINGS', (255, 0, 0), (0, 0, 255), show_settings],
                                                   [100, 310, 'EXIT', (255, 0, 0), (0, 0, 255), sys.exit]])
        menu.generate_sky()
        menu.show_menu()

    elif _cycle_ == "Pause":
        menu = Menu(screen, "Pause", buttons=[[100, 100, "CONTINUE", (0, 100, 0), (0, 0, 255), continue_game],
                                              [100, 170, "MAIN MENU", (255, 0, 0,), (0, 0, 255), return_to_main_menu],
                                              [100, 240, "STAR SYSTEMS MAP", (255, 0, 0), (0, 0, 255),
                                               show_star_system_map],
                                              [100, 310, "SETTINGS", (255, 0, 0), (0, 0, 255), show_settings]],
                    k_escape_fun=continue_game)
        menu.generate_sky()
        menu.show_menu()

    elif _cycle_ == "Main Cycle":
        if printed_time:
            t = 0
            t1 = 0
        key = pygame.key.get_pressed()
        screen.fill((5, 5, 5))
        player_group.update(key)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
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
        screen.blit(*status.to_blit["num_known"])
        if len(known) == len(planet_group.sprites()):
            printed_time = True
        minimap()
        pygame.display.flip()
        if key[pygame.K_SPACE] and not paused:
            scan_channel = scan_sound.play(0)
        clock.tick(50)

    elif _cycle_ == "Star System Map":
        map = StarSystemMap(screen)
        map.show_map()

    else:
        menu = Menu(screen, _cycle_,
                    buttons=[[100, 100, 'UNEXPECTED ERROR', (255, 255, 255), (255, 255, 255), do_nothing],
                             [100, 170, 'RETURN TO MAIN MENU', (255, 0, 0), (0, 0, 255),
                              return_to_main_menu]], k_escape_fun=do_nothing)
        menu.show_menu()

pygame.quit()
