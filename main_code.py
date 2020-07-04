
from os import path


WIDTH = 1200
HEIGHT = 750
FPS = 60
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
start_coord_vrags = []
coord_walls = []
import pygame
import random
import time
import sys
import winsound

pygame.init()
pygame.mixer.init()

img_dir = path.join(path.dirname(__file__), 'img')
font_name = pygame.font.match_font('arial')

start_main = False
win = False



def get_equal_line(x1, y1, x2, y2):
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1
    return (a, b, c)


def write(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def is_rectangle_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    if x3 > x2:
        return False
    if y4 > y1:
        return False
    if x1 > x4:
        return False
    if y2 > y3:
        return False
    return True

def is_intersection(tup1, tup2):
    a1 = tup1[0]
    b1 = tup1[1]
    c1 = tup1[2]
    a2 = tup2[0]
    b2 = tup2[1]
    c2 = tup2[2]
    if a2 * b1 == a1 * b2 or a1 == 0:
        return tup_none
    else:
        y = (a1 * c2 - a2 * c1) / (a2 * b1 - a1 * b2)
        x = (-c1 - b1 * y) / a1
        return (x, y)


def is_Point_in_cut(x, y, x1, y1, x2, y2):
    #print("min func", min(x1, x2), ' ', max(x1, x2))
    #print("max func", max(x1, x2), ' ', max(x1, x2))
    eps = 15
    if x >= min(x1, x2) - eps and x <= max(x1, x2) + eps:
        if y >= min(y1, y2) - eps and y <= max(y1, y2) + eps:
            #print("TRUEEEEEEEEEEEE")
            return (x, y)

    return tup_none


def get_now_speed(x, y):
    leftx = -4
    rightx = 4
    lefty = -4
    righty = 4
    if x < 10:
        if x == 0:
            leftx = 2
        else:
            leftx = 1
    if x > WIDTH - 60:
        if x == WIDTH - 50:
            rightx = -2
        else:
            rightx = -1
    if y < 10:
        if y == 0:
            lefty = 2
        else:
            lefty = 1
    if y > HEIGHT - 60:
        if y == HEIGHT - 50:
            righty = -2
        else:
            righty = -1
    finalx = random.randint(leftx, rightx)
    finaly = random.randint(lefty, righty)
    return (finalx, finaly)




class Our_Tank(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = my_pic
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH, random.randint(0, HEIGHT))
    def update(self):
        global now_coord_of_player, patron
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        if keystate[pygame.K_w] or keystate[pygame.K_a] or keystate[pygame.K_s] or keystate[pygame.K_d]:
            if time.time() - time_last_shoot > 0.2 and patron > 0:
                patron -= 1
                pulya = Pulya(self.rect.x, self.rect.y, None, None)
                all_sprites.add(pulya)
                Pulya_group.add(pulya)
        if self.rect.x + self.speedx > WIDTH - 50:
            self.rect.x = WIDTH - 50
        else:
            self.rect.x += self.speedx
        if (self.rect.y + self.speedy > HEIGHT - 50):
            self.rect.y = HEIGHT - 50
        else:
            self.rect.y += self.speedy
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = 0
        now_coord_of_player = (self.rect.x, self.rect.y)

class Vragi(pygame.sprite.Sprite):
    def __init__(self, number):
        global start_coord_vrags
        pygame.sprite.Sprite.__init__(self)
        self.image = vrag_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)

        while True:
            good_pair = True
            startx = random.randint(0, WIDTH - 100)
            starty = random.randint(0, HEIGHT)
            #print(startx, starty)
            for i in start_coord_vrags:
                if is_rectangle_intersect(startx, starty, startx + 50, starty + 50, i[0], i[1], i[0] + 50, i[1] + 50):
                    good_pair = False
            for i in coord_walls:
                #print(i)
                if i[2] == 1:
                    wid = 90
                    hei = 5
                else:
                    wid = 5
                    hei = 90
                #print(startx, starty, startx + 50, starty + 50, i[0], i[1], i[0] + wid, i[1] + hei)
                if is_rectangle_intersect(startx, starty, startx + 50, starty + 50, i[0], i[1], i[0] + wid, i[1] + hei):
                    good_pair = False
            if good_pair:
                start_coord_vrags.append((startx, starty))
                break
        self.rect.center = (random.randint(0, WIDTH - 100), random.randint(0, HEIGHT))
        self.number = number
    def update(self):
        global last_time, coord
        if time.time() - time_list_shoot_vragi[int(self.number) - 1] > time_delta:
            random_counter = random.randint(0, 100)
            if random_counter > 85 and time.time() - time_wait_to_load_game > 0.3:
                pulya = Pulya(self.rect.x, self.rect.y, now_coord_of_player[0], now_coord_of_player[1])
                all_sprites.add(pulya)
                Pulya_group_vrag.add(pulya)
                time_list_shoot_vragi[int(self.number) - 1] = time.time()
        if time.time() - time_list[int(self.number) - 1] > 0.3:
            help_tuple = get_now_speed(self.rect.x, self.rect.y)
            self.speedx = help_tuple[0]
            self.speedy = help_tuple[1]
            time_list[int(self.number) - 1] = time.time()
        else:
            if time.time() - time_wait_to_load_game > 0.5:
                while True:
                    line = get_equal_line(self.rect.x, self.rect.y, self.rect.x + self.speedx,
                                          self.rect.y + self.speedy)
                    line2 = get_equal_line(self.rect.x + 50, self.rect.y + 50,
                                           self.rect.x + 50 + self.speedx, self.rect.y + 50 + self.speedy)
                    #print("line_vrag == ", line)
                    Flag = True
                    for j in help_coord_equals:
                        #print("line_wall = ", j)
                        tuple_intersect = is_intersection(line, j)
                        tuple_intersect2 = is_intersection(line2, j)
                        if tuple_intersect[0] != None or tuple_intersect2[0] != None:
                            ind = help_coord_equals.index(j)
                            help_x1 = coord_walls[ind][0]
                            help_y1 = coord_walls[ind][1]
                            if coord_walls[ind][2]:
                                help_x2 = help_x1 + 90
                                help_y2 = help_y1 + 5
                            else:
                                help_x2 = help_x1 + 5
                                help_y2 = help_y1 + 90
                            #print("coord_walls == ", help_x1, help_y1, help_x2, help_y2)
                            #print("Точка пересечения == ", tuple_intersect)
                            help_function_is_cut_intersect = is_Point_in_cut(tuple_intersect[0], tuple_intersect[1], help_x1, help_y1,
                                                                             help_x2, help_y2)
                            #print(help_function_is_cut_intersect)
                            help_function_is_cut_intersect2 = is_Point_in_cut(tuple_intersect2[0], tuple_intersect2[1],help_x1, help_y1,
                                                                             help_x2, help_y2)
                            if help_function_is_cut_intersect != tup_none or help_function_is_cut_intersect2 != tup_none:
                                Flag = False
                    if not Flag:
                        (self.speedx, self.speedy) = get_now_speed(self.rect.x, self.rect.y)
                        #print("UPDATE ============== ", self.speedx, self.speedy)
                    else:
                        #print(Flag)
                        break
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                if self.rect.x + self.speedx > WIDTH - 50:
                    self.rect.x = WIDTH - 50
                else:
                    self.rect.x += self.speedx
                if (self.rect.y + self.speedy > HEIGHT - 50):
                    self.rect.y = HEIGHT - 50
                else:
                    self.rect.y += self.speedy
                if self.rect.x < 0:
                    self.rect.x = 0
                if self.rect.y < 0:
                    self.rect.y = 0





class Pulya(pygame.sprite.Sprite):
    def __init__(self, startx, starty, coordxplayer, coordyplayer):
        self.startx = startx
        self.starty = starty
        global time_last_shoot
        #ЧТО ДЕЛАТЬ????????????
        pygame.sprite.Sprite.__init__(self)
        if coordxplayer == None or coordyplayer == None:
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_d]:
                self.right_direction()
            elif keystate[pygame.K_a]:
                self.left_direction()
            elif keystate[pygame.K_s]:
                self.down_direction()
            elif keystate[pygame.K_w]:
                self.up_direction()
            #print(self.speedx, self.speedy)
            time_last_shoot = time.time()
        else:
            shiftx = coordxplayer - startx
            shifty = coordyplayer - starty
            if shiftx > 0:
                if shifty > 0:
                    if shiftx > shifty:
                        self.right_direction()
                    else:
                        self.up_direction()
                else:
                    if abs(shifty) > shiftx:
                        self.down_direction()
                    else:
                        self.right_direction()
            else:
                if shifty > 0:
                    if shifty > abs(shiftx):
                        self.up_direction()
                    else:
                        self.left_direction()
                else:
                    if abs(shifty) > abs(shiftx):
                        self.down_direction()
                    else:
                        self.left_direction()

    def right_direction(self):
        self.speedx = 10
        self.speedy = 0
        self.image = pygame.Surface((15, 5))
        self.rect = self.image.get_rect()
        self.rect.center = (self.startx + 10, self.starty + 25)
        self.image.fill(YELLOW)

    def left_direction(self):
        self.speedx = -10
        self.speedy = 0
        self.image = pygame.Surface((15, 5))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (self.startx - 10, self.starty + 25)

    def down_direction(self):
        self.speedx = 0
        self.speedy = 10
        self.image = pygame.Surface((5, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (self.startx + 25, self.starty + 10)

    def up_direction(self):
        self.speedx = 0
        self.speedy = -10
        self.image = pygame.Surface((5, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (self.startx + 25, self.starty - 10)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy



class Walls(pygame.sprite.Sprite):
    def __init__(self):
        global coord_walls, help_coord_equals
        pygame.sprite.Sprite.__init__(self)
        while True:
            xcoord = random.randint(200, WIDTH - 100)
            ycoord = random.randint(200, HEIGHT - 100)
            push = True
            for i in coord_walls:
                if abs(xcoord - i[0]) < 90 or abs(ycoord - i[1]) < 90:
                    push = False
            if push:
                break
        place = random.randint(0, 1)
        if place == 1:
            help_coord_equals.append(get_equal_line(xcoord, ycoord, xcoord + 90, ycoord + 5))
        else:
            help_coord_equals.append(get_equal_line(xcoord, ycoord, xcoord + 5, ycoord + 90))
        coord_walls.append((xcoord, ycoord, place))
        self.leftx = xcoord
        self.lefty = ycoord
        self.image = pygame.Surface(help_coord_walls[place])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (self.leftx, self.lefty)

def start_settings():
    global screen, clock, all_sprites, vrags, Pulya_group_vrag, Pulya_group, walls_group, player, time_delta, now_coord_of_player, patron
    global last_time, time_list, time_list_shoot_vragi, tup_none, time_last_shoot, count_vrags, count_walls, help_coord_walls
    global help_coord_equals, coord_walls, time_wait_to_load_game, start_coord_vrags, vrag_img, background, background_rect
    global my_pic

    start_coord_vrags = []
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background = pygame.image.load(path.join(img_dir, 'background.jpg')).convert()
    background_rect = background.get_rect()
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    pygame.display.set_caption("Idk")
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    vrags = pygame.sprite.Group()
    Pulya_group = pygame.sprite.Group()
    Pulya_group_vrag = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    my_pic = pygame.image.load(path.join(img_dir, "my_pic.png")).convert()
    player = Our_Tank()
    all_sprites.add(player)
    time_delta = 1.5
    now_coord_of_player = (0, 0)

    patron = 50
    last_time = time.time()
    time_list = []
    time_list_shoot_vragi = []
    tup_none = (None, None)
    time_last_shoot = time.time()

    count_vrags = random.randint(3, 5)
    # count_vrags = 1
    count_walls = random.randint(2, 4)
    # count_walls = 1

    help_coord_walls = [(5, 90), (90, 5)]

    help_coord_equals = []

    coord_walls = []
    time_wait_to_load_game = time.time()
    for i in range(count_walls):
        wall = Walls()
        walls_group.add(wall)
        all_sprites.add(wall)
    vrag_img = pygame.image.load(path.join(img_dir, "vrag_image.png")).convert()
    for i in range (count_vrags):
        vrag = Vragi(i + 1)
        time_list.append(last_time)
        vrags.add(vrag)
        all_sprites.add(vrag)
        time_list_shoot_vragi.append(last_time)




def start_screen():
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    write(screen, "Добро пожаловать в игру: название не придумал!", 30, WIDTH / 2, HEIGHT / 4)
    write(screen, "Правила:", 22,
              WIDTH / 2, HEIGHT / 2 + 50)
    write(screen, "При столкновении с ботом или стеной Вы умираете", 22,
              WIDTH / 2, HEIGHT / 2 + 100)
    write(screen, "Количество патронов ограничено, расходуйте их разумно", 22,
              WIDTH / 2, HEIGHT / 2 + 150)
    write(screen, "С каждой секундой, интенсивность стрельбы врагов увеличивается", 22,
              WIDTH / 2, HEIGHT / 2 + 200)
    write(screen, "Нажмите пробел, чтобы продолжить", 18, WIDTH / 2, HEIGHT / 2 + 250)
    write(screen, "Управление: ", 18, WIDTH - 100, HEIGHT // 2 - 100)
    write(screen, "WASD - стрельба", 18, WIDTH - 100, HEIGHT // 2 - 50)
    write(screen, "↑, ↓, ←, → - движение", 18, WIDTH - 100, HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        keystate = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if keystate[pygame.K_SPACE]:
                waiting = False

def win_screen():
    global start_main
    start_main = False
    write(screen, "Вы победили!", 30, WIDTH // 2, HEIGHT // 2)
    write(screen, "Нажмите пробел, чтобы начать игру заново", 18, WIDTH / 2, HEIGHT / 2 + 250)
    write(screen, "Нажмите escape, чтобы вернуться к правилам", 18, WIDTH / 2, HEIGHT / 2 + 300)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        keystate = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if keystate[pygame.K_SPACE]:
                start_main = True
                waiting = False
            elif keystate[pygame.K_ESCAPE]:
                waiting = False
def lose_screen():
    global start_main
    start_main = False
    write(screen, "К сожалению, Вы проиграли. Хотите сыграть еще раз?", 30, WIDTH // 2, HEIGHT // 2)
    write(screen, "Нажмите пробел, чтобы начать игру заново", 18, WIDTH / 2, HEIGHT / 2 + 250)
    write(screen, "Нажмите escape, чтобы вернуться к правилам", 18, WIDTH / 2, HEIGHT / 2 + 300)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        keystate = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if keystate[pygame.K_SPACE]:
                start_main = True
                waiting = False
            elif keystate[pygame.K_ESCAPE]:
                waiting = False
def main():
    global time_delta, win, start_main
    running = True
    start_main = False

    while running:

        win = False
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
                exit(0)


        if pygame.sprite.spritecollide(player, vrags, False) or pygame.sprite.spritecollide(player, Pulya_group_vrag, False):
            #print("YOU LOST")
            winsound.Beep(2500, 500)
            running = False
        dead_vrags = pygame.sprite.groupcollide(Pulya_group, vrags, True, True)
        pulya_walls = pygame.sprite.groupcollide(walls_group, Pulya_group, False, True)
        pulya_walls_vrag = pygame.sprite.groupcollide(walls_group, Pulya_group_vrag, False, True)
        if pygame.sprite.spritecollide(player, walls_group, False):
            #print("YOU LOST")
            winsound.Beep(2500, 500)
            running = False
        pygame.sprite.groupcollide(walls_group, vrags, False, True)
        if time_delta > 0.2:
            time_delta -= 0.001
        if len(vrags) == 0:
            win = True
            running = False
        all_sprites.update()
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        write(screen, str(patron), 30, WIDTH - 30, 0)
        pygame.display.flip()

while True:
    start_settings()
    #print("START MAIN == ", start_main)
    if not start_main:
        start_screen()
    main()
    #print("WIN == ", win)
    if win:
        start_settings()
        win_screen()
    else:
        start_settings()
        lose_screen()


pygame.quit()
