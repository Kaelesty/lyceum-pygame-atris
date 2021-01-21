import pygame
import random
import copy
import sqlite3
import datetime as dt

OS = 1 / 0.8917795292374964
OOS = 0.8917795292374964
WIDTH = 4


# minos
# 1 - line
# 2 - cube
# 3 - g
# 4 - cross
# 5 - z

# Figures note:
# "_" in [0] -> block is static
# "_" in [-1] -> block is center of figure


class Panic(Exception):
    pass


class Welltris:
    def __init__(self, screen, mode, pos):
        self.surface = screen
        self.wings = [[["0"] * 8 for _ in range(8)],
                      [["0"] * 8 for _ in range(8)],
                      [['0'] * 8 for _ in range(8)],
                      [["0"] * 8 for _ in range(8)],
                      [["0"] * 8 for _ in range(8)]]
        self.hat = [["0"] * 8 for _ in range(5)]
        self.mode = mode
        self.pos = pos
        self.game = 1
        self.next = random.randrange(1, 6)
        self.score = 0
        self.new_current()
        self.pause = 0.9
        self.begin = dt.datetime.now()

    def terminate(self):
        con = sqlite3.connect("Data\ "[0:-1] + "AData.sqlite")
        cur = con.cursor()
        data = cur.execute(f"SELECT _{self.mode} FROM Scores").fetchall()
        if list(data)[0][0] < self.score:
            cur.execute(f"UPDATE Scores SET _{self.mode} = {self.score}")
        con.commit()
        con.close()
        # i will be back

    def new_current(self):
        self.current_wing = random.choice([1, 2, 3, 4])
        color = random.choice(['1', '2', '3'])
        figure, self.next = self.next, random.randrange(1, 6)
        x = random.randrange(1, 6)
        self.hat[1][x] = color + '_'
        if figure == 1:
            self.hat[0][x] = color
            self.hat[2][x] = color
            self.hat[3][x] = color
        elif figure == 2:
            self.hat[0][x] = color
            self.hat[1][x + 1] = color
            self.hat[0][x + 1] = color
        elif figure == 3:
            self.hat[0][x] = color
            self.hat[0][x - 1] = color
            self.hat[2][x] = color
        elif figure == 4:
            self.hat[1][x + 1] = color
            self.hat[1][x - 1] = color
            self.hat[2][x] = color
        else:
            self.hat[2][x] = color
            self.hat[1][x - 1] = color
            self.hat[0][x - 1] = color
        self.figure = figure

    def make_step(self):
        self.check_fulls()
        now = dt.datetime.now()
        print(self.pause)
        if self.game == 1 and (now - self.begin).total_seconds() >= self.pause:
            #  check wing possible
            self.begin = now
            if self.pause > 0:
                self.pause -= 0.002
            _can = True
            points = []
            cpoints = []
            for i in range(8):
                for j in range(8):
                    if self.wings[self.current_wing][i][j] != '0' and self.wings[self.current_wing][i][j][0] != '_':
                        points.append((i, j, self.wings[self.current_wing][i][j]))
            for elem in points:
                if elem[0] != 7:
                    if self.wings[self.current_wing][elem[0] + 1][elem[1]][0] == '_':
                        _can = False
                else:
                    if self.current_wing == 1 and self.wings[0][elem[1]][0] == "_":
                        _can = False
                    elif self.current_wing == 2 and self.wings[0][elem[1]][7][0] == "_":
                        _can = False
                    elif self.current_wing == 3 and self.wings[0][7][7 - elem[1]][0] == "_":
                        _can = False
                    elif self.current_wing == 4 and self.wings[0][7 - elem[1]][0][0] == "_":
                        _can = False
            if _can:
                # check hat possible
                hpoints = []
                for i in range(5):
                    for j in range(8):
                        if self.hat[i][j] != '0':
                            hpoints.append((i, j, self.hat[i][j]))
                for elem in hpoints:
                    if elem[0] == 5:
                        if self.wings[self.current_wing][0][elem[1]][0] == '_':
                            _can = False
            if _can:
                # check center possible
                try:
                    for i in range(8):
                        for j in range(8):
                            if self.wings[0][i][j] != "0" and self.wings[0][i][j][0] != '_':
                                cpoints.append((i, j,  self.wings[0][i][j]))
                except Exception:
                    for elem in self.wings[0]:
                        print(elem)
                if self.current_wing == 1:
                    x_move = 0
                    y_move = 1
                elif self.current_wing == 2:
                    x_move = -1
                    y_move = 0
                elif self.current_wing == 3:
                    x_move = 0
                    y_move = -1
                else:
                    x_move = 1
                    y_move = 0
                for elem in cpoints:
                    if x_move == 1 and elem[1] == 7:
                        _can = False
                    elif x_move == -1 and elem[1] == 0:
                        _can = False
                    elif y_move == 1 and elem[0] == 7:
                        _can = False
                    elif y_move == -1 and elem[0] == 0:
                        _can = False
                    elif self.wings[0][elem[0] + y_move][elem[1] + x_move][0] == "_":
                        _can = False
            if _can:
                for elem in cpoints:
                    self.wings[0][elem[0]][elem[1]] = "0"
                cpoints = sorted(cpoints, key=lambda x: -int(x[1]))
                for elem in cpoints:
                    self.wings[0][elem[0] + y_move][elem[1] + x_move] = elem[2]
                for elem in points:
                    self.wings[self.current_wing][elem[0]][elem[1]] = '0'
                points = sorted(points, key=lambda x: -int(x[1]))
                for elem in points:
                    if elem[0] != 7:
                        self.wings[self.current_wing][elem[0] + 1][elem[1]] = elem[2]
                    else:
                        if self.current_wing == 1:
                            self.wings[0][0][elem[1]] = elem[2]
                        elif self.current_wing == 2:
                            self.wings[0][elem[1]][7] = elem[2]
                        elif self.current_wing == 3:
                            self.wings[0][7][7 - elem[1]] = elem[2]
                        elif self.current_wing == 4:
                            self.wings[0][7 - elem[1]][0] = elem[2]
                for elem in hpoints:
                    self.hat[elem[0]][elem[1]] = '0'
                hpoints = sorted(hpoints, key=lambda x: -int(x[1]))
                for elem in hpoints:
                    if elem[0] != 4:
                        self.hat[elem[0] + 1][elem[1]] = elem[2]
                    else:
                        self.wings[self.current_wing][0][elem[1]] = elem[2]
            else:
                for elem in points:
                    self.wings[self.current_wing][elem[0]][elem[1]] = '_' + self.wings[self.current_wing][elem[0]][elem[1]]
                self.hat = [["0"] * 8 for _ in range(5)]
                for elem in cpoints:
                    self.wings[0][elem[0]][elem[1]] = "_" + elem[2]
                self.new_current()
            list(map(lambda x: x[0], self.wings[self.current_wing][i]))

    def check_fulls(self):
        if self.wings[self.current_wing] != [['0'] * 8 for _ in range(8)]:
            for i in range(8):
                if list(map(lambda x: x[0], self.wings[self.current_wing][i])) == ["_"] * 8:
                    del self.wings[self.current_wing][i]
                    self.wings[self.current_wing].insert(0, ["0"] * 8)
                    self.score += 8
        if self.wings[0] != [["0"] * 8 for _ in range(8)]:
            fulls = []
            for i in range(8):
                if list(map(lambda x: x[0], self.wings[0][i])) == ["_"] * 8:
                    del self.wings[0][i]
                    self.wings[0].insert(0, ["0"] * 8)
                    self.score += 8
                _full = True
                for j in range(8):
                    if self.wings[0][j][i][0] != "_":
                        _full = False
                if _full:
                    fulls.append(i)
            for i in fulls:
                for j in range(8):
                    self.wings[0][j][i] = ["0"] * 8



    def game_over(self):
        pass

    def catch(self, event): # A - 97, D - 100, SPACE - 32
        if event.key == 27:
            if self.game == 0:
                self.game = 1
            else:
                self.game = 0
        elif event.key == 97 and (self.game == 1 or self.mode == "easy"):
            _can = True
            cpoints = []
            if self.current_wing == 1:
                x_move = -1
                y_move = 0
            elif self.current_wing == 2:
                x_move = 0
                y_move = -1
            elif self.current_wing == 3:
                x_move = 1
                y_move = 0
            elif self.current_wing == 4:
                x_move = 0
                y_move = 1
            for i in range(8):
                for j in range(8):
                    if self.wings[0][i][j] != '0' and self.wings[0][i][j][0] != '_':
                        cpoints.append((i, j, self.wings[0][i][j]))
            for elem in cpoints:
                if not 0 <= elem[0] + y_move <= 7 or not 0 <= elem[1] + x_move <= 7:
                    _can = False
                else:
                    if self.wings[0][elem[0] + y_move][elem[1] + x_move][0] == '_':
                        _can = False
            #  check wing possible
            points = []
            for i in range(8):
                for j in range(8):
                    if self.wings[self.current_wing][i][j] != '0' and self.wings[self.current_wing][i][j][0] != '_':
                        points.append((i, j, self.wings[self.current_wing][i][j]))
            for elem in points:
                if elem[1] == 0:
                    _can = False
                else:
                    if self.wings[self.current_wing][elem[0]][elem[1] - 1][0] == '_':
                        _can = False
            if _can:
                # check hat possible
                hpoints = []
                for i in range(5):
                    for j in range(8):
                        if self.hat[i][j] != '0':
                            hpoints.append((i, j, self.hat[i][j]))
                for elem in hpoints:
                    if elem[1] == 0:
                        if self.wings[self.current_wing][0][elem[1]][0] == '_':
                            _can = False
            if _can:
                for elem in cpoints:
                    self.wings[0][elem[0]][elem[1]] = '0'
                cpoints = sorted(cpoints, key=lambda x: -int(x[1]))
                for elem in cpoints:
                    self.wings[0][elem[0] + y_move][elem[1] + x_move] = elem[2]
                for elem in points:
                    self.wings[self.current_wing][elem[0]][elem[1]] = '0'
                points = sorted(points, key=lambda x: -int(x[1]))
                for elem in points:
                    self.wings[self.current_wing][elem[0]][elem[1] - 1] = elem[2]
                for elem in hpoints:
                    self.hat[elem[0]][elem[1]] = '0'
                hpoints = sorted(hpoints, key=lambda x: -int(x[1]))
                for elem in hpoints:
                    if elem[0] != 4:
                        self.hat[elem[0]][elem[1] - 1] = elem[2]
                    else:
                        self.wings[self.current_wing][0][elem[1]] = elem[2]
        elif event.key == 100 and (self.game == 1 or self.mode == "easy"):
            _can = True
            cpoints = []
            if self.current_wing == 1:
                x_move = 1
                y_move = 0
            elif self.current_wing == 2:
                x_move = 0
                y_move = 1
            elif self.current_wing == 3:
                x_move = -1
                y_move = 0
            elif self.current_wing == 4:
                x_move = 0
                y_move = -1
            for i in range(8):
                for j in range(8):
                    if self.wings[0][i][j] != '0' and self.wings[0][i][j][0] != '_':
                        cpoints.append((i, j, self.wings[0][i][j]))
            for elem in cpoints:
                if (not elem[0] + y_move in [i for i in range(8)]) or (not elem[1] + x_move in [i for i in range(8)]):
                    _can = False
                else:
                    if self.wings[0][elem[0] + y_move][elem[1] + x_move][0] == '_':
                        _can = False
            #  check wing possible
            points = []
            for i in range(8):
                for j in range(8):
                    if self.wings[self.current_wing][i][j] != '0' and self.wings[self.current_wing][i][j][0] != '_':
                        points.append((i, j, self.wings[self.current_wing][i][j]))
            for elem in points:
                if elem[1] == 7:
                    _can = False
                else:
                    if self.wings[self.current_wing][elem[0]][elem[1] - 1][0] == '_':
                        _can = False
            if _can:
                # check hat possible
                hpoints = []
                for i in range(5):
                    for j in range(8):
                        if self.hat[i][j] != '0':
                            hpoints.append((i, j, self.hat[i][j]))
                for elem in hpoints:
                    if elem[1] == 7:
                        if self.wings[self.current_wing][0][elem[1]][0] == '_':
                            _can = False
            if _can:
                for elem in cpoints:
                    self.wings[0][elem[0]][elem[1]] = '0'
                cpoints = sorted(cpoints, key=lambda x: -int(x[1]))
                for elem in cpoints:
                    self.wings[0][elem[0] + y_move][elem[1] + x_move] = elem[2]
                for elem in points:
                    self.wings[self.current_wing][elem[0]][elem[1]] = '0'
                points = sorted(points, key=lambda x: -int(x[1]))
                for elem in points:
                    self.wings[self.current_wing][elem[0]][elem[1] + 1] = elem[2]
                for elem in hpoints:
                    self.hat[elem[0]][elem[1]] = '0'
                hpoints = sorted(hpoints, key=lambda x: -int(x[1]))
                for elem in hpoints:
                    if elem[0] != 4:
                        self.hat[elem[0]][elem[1] + 1] = elem[2]
                    else:
                        self.wings[self.current_wing][0][elem[1]] = elem[2]
        elif event.key == 32 and (self.game == 1 or self.mode == "easy"):
            try:
                # rotation
                c_points = []
                w_points = []
                if self.hat == [["0"] * 8 for _ in range(5)]:
                    for i in range(8):
                        for j in range(8):
                            if not (self.wings[0][i][j][0] in ["0", "_"]):
                                c_points.append((i, j, self.wings[0][i][j]))
                            if not (self.wings[self.current_wing][i][j][0] in ["0", "_"]):
                                w_points.append((i, j, self.wings[self.current_wing][i][j]))
                    if c_points == []:
                        old_points = copy.deepcopy(w_points)
                        board_id = self.current_wing
                    elif w_points == []:
                        old_points = copy.deepcopy(c_points)
                        board_id = 0
                    else:
                        raise Panic
                    for i in range(4):
                        if old_points[i][2][-1] == "_":
                            center = old_points[i]
                            del old_points[i]
                            break
                    # {figure detector}
                    if self.figure == 1:
                        if (center[0] - 1, center[1], center[2][:-1]) in old_points:  # now is vetrical
                            new_points = list()
                            new_points.append((center[0], center[1] - 1))
                            new_points.append((center[0], center[1] + 1))
                            new_points.append((center[0], center[1] + 2))
                        else:  # now is horizontal
                            new_points = []
                            new_points.append((center[0] - 1, center[1]))
                            new_points.append((center[0] + 1, center[1]))
                            new_points.append((center[0] + 2, center[1]))
                    elif self.figure == 3:
                        if (center[0] - 1, center[1], center[2][:-1]) in old_points: # now is hori
                            new_points = []
                            new_points.append((center[0], center[1] - 1))
                            new_points.append((center[0], center[1] + 1))
                        else:
                            new_points = []
                            new_points.append((center[0] - 1, center[1]))
                            new_points.append((center[0] + 1, center[1]))
                        if (center[0] + 1, center[1] + 1, center[2][:-1]) in old_points:
                            new_points.append((center[0] + 1, center[1] - 1))
                        elif (center[0] + 1, center[1] - 1, center[2][:-1]) in old_points:
                            new_points.append((center[0] - 1, center[1] - 1))
                        elif (center[0] - 1, center[1] - 1, center[2][:-1]) in old_points:
                            new_points.append((center[0] - 1, center[1] + 1))
                        elif (center[0] - 1, center[1] + 1, center[2][:-1]) in old_points:
                            new_points.append((center[0] + 1, center[1] + 1))
                    elif self.figure == 4:
                        new_points = []
                        new_points.append((center[0] + 1, center[1]))
                        new_points.append((center[0] - 1, center[1]))
                        new_points.append((center[0], center[1] + 1))
                        new_points.append((center[0], center[1] - 1))
                        if not (center[0], center[1] - 1, center[2][:-1]) in old_points:
                            del new_points[1]
                        elif not (center[0] - 1, center[1], center[2][:-1]) in old_points:
                            del new_points[2]
                        elif not (center[0], center[1] + 1, center[2][:-1]) in old_points:
                            del new_points[0]
                        elif not (center[0] + 1, center[1], center[2][:-1]) in old_points:
                            del new_points[3]
                    elif self.figure == 5:
                        if (center[0], center[1] - 1, center[2][:-1]) in old_points and (center[0] - 1, center[1] - 1, center[2][:-1]) in old_points:
                            new_points = []
                            new_points.append((center[0], center[1] - 1))
                            new_points.append((center[0] - 1, center[1] + 1))
                            new_points.append((center[0] - 1, center[1]))
                        elif (center[0] + 1, center[1] + 1, center[2][:-1]) in old_points and (center[0] + 1, center[1], center[2][:-1]) in old_points:
                            new_points = []
                            new_points.append((center[0], center[1] - 1))
                            new_points.append((center[0] - 1, center[1] - 1))
                            new_points.append((center[0] + 1, center[1]))
                        elif (center[0], center[1] + 1, center[2][:-1]) in old_points and (center[0] - 1, center[1] + 1, center[2][:-1]) in old_points:
                            new_points = []
                            new_points.append((center[0], center[1] - 1))
                            new_points.append((center[0] + 1, center[1] + 1))
                            new_points.append((center[0] + 1, center[1]))
                        elif (center[0] - 1, center[1], center[2][:-1]) in old_points and (center[0] - 1, center[1] + 1, center[2][:-1]) in old_points:
                            new_points = []
                            new_points.append((center[0] - 1, center[1] + 1))
                            new_points.append((center[0], center[1] + 1))
                            new_points.append((center[0] + 1, center[1]))
                    _can = True
                    for elem in new_points:
                        if self.wings[board_id][elem[0]][elem[1]][0] == "_" or not 0 <= elem[0] <= 7 or not 0 <= elem[1] <= 7:
                            _can = False
                    if _can:
                        for i in range(3):
                            self.wings[board_id][old_points[i][0]][old_points[i][1]] = '0'
                        for i in range(3):
                            self.wings[board_id][new_points[i][0]][new_points[i][1]] = old_points[i][2]
                        self.wings[board_id][center[0]][center[1]] = center[2]
                    else:
                        raise Panic
                else:
                    raise Panic
            except Exception as ex:
                pass

    def draw_self(self):
        pygame.draw.rect(self.surface, (255, 190, 15),
                         (self.pos[0], self.pos[1], 700, 700), width=WIDTH)
        self.draw_center()
        self.draw_top()
        self.draw_bottom()
        self.draw_left()
        self.draw_right()
        self.draw_score()
        self.draw_secondary()
        pygame.draw.rect(self.surface, (255, 190, 15),
                         (self.pos[0] + 700, self.pos[1], 320, 100), width=WIDTH)
        sprites = pygame.sprite.Group()
        sprite1 = pygame.sprite.Sprite()
        sprite1.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                          "status.png")
        sprite1.rect = sprite1.image.get_rect()
        sprite1.rect.x = self.pos[0] + 710
        sprite1.rect.y = self.pos[1] + 5
        sprites.add(sprite1)
        if self.game == 0:
            sprite1 = pygame.sprite.Sprite()
            sprite1.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                              "paused.png")
            sprite1.rect = sprite1.image.get_rect()
            sprite1.rect.x = self.pos[0] + 710
            sprite1.rect.y = self.pos[1] + 25
            sprites.add(sprite1)
        else:
            sprite1 = pygame.sprite.Sprite()
            sprite1.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                              "gim.png")
            sprite1.rect = sprite1.image.get_rect()
            sprite1.rect.x = self.pos[0] + 710
            sprite1.rect.y = self.pos[1] + 25
            sprites.add(sprite1)
        sprites.draw(self.surface)

    def draw_secondary(self):
        if self.mode != "hard":
            coords = list()
            if self.next == 1:
                coords.append((1, 2))
                coords.append((2, 2))
                coords.append((3, 2))
                coords.append((4, 2))
            elif self.next == 2:
                coords.append((2, 2))
                coords.append((2, 3))
                coords.append((3, 2))
                coords.append((3, 3))
            elif self.next == 3:
                coords.append((1, 2))
                coords.append((2, 2))
                coords.append((3, 2))
                coords.append((3, 3))
            elif self.next == 4:
                coords.append((2, 2))
                coords.append((3, 2))
                coords.append((4, 2))
                coords.append((3, 3))
            elif self.next == 5:
                coords.append((2, 2))
                coords.append((3, 2))
                coords.append((3, 3))
                coords.append((4, 3))
            sprites = pygame.sprite.Group()
            for i in range(6):
                for j in range(6):
                    pygame.draw.rect(self.surface, (255, 190, 15),
                                     (self.pos[0] + 700 + 35 * j, self.pos[1] + 200 + 35 * i, 35, 35), width=1)
                    if (i, j) in coords:
                        sprite = pygame.sprite.Sprite()
                        sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                                         "cube_-1.png")
                        sprite.rect = sprite.image.get_rect()
                        sprite.rect.x = self.pos[0] + 700 + 35 * j
                        sprite.rect.y = self.pos[1] + 200 + 35 * i
                        sprites.add(sprite)
            sprites.draw(self.surface)

    def draw_score(self):
        pygame.draw.rect(self.surface, (255, 190, 15),
                         (self.pos[0] + 700, self.pos[1] + 100, 320, 100), width=WIDTH)
        font = pygame.font.Font("Data\ "[0:-1] + "Konstanting.ttf", 50)
        text = font.render("Score:", True, (255, 190, 15))
        text_x = self.pos[0] + 710
        text_y = self.pos[1] + 110
        text_w = text.get_width()
        text_h = text.get_height()
        self.surface.blit(text, (text_x, text_y))
        text = font.render(str(self.score), True, (255, 190, 15))
        text_x = self.pos[0] + 710
        text_y = self.pos[1] + 150
        text_w = text.get_width()
        text_h = text.get_height()
        self.surface.blit(text, (text_x, text_y))

    def draw_center(self):
        for i in range(8):
            for j in range(8):
                if self.wings[0][i][j] != '0':
                    width = 0
                else:
                    width = WIDTH
                pygame.draw.rect(self.surface, (235, 160, 0),
                                 (self.pos[0] + 210 + 35 * j, self.pos[1] + 210 + 35 * i, 35, 35), width=width)

    def draw_top(self):
        for i in range(8):
            for j in range(8):
                indent_1 = (700 - 700 * OOS ** i) // 2
                side_1 = 87.5 * OOS ** i
                indent_2 = (700 - 700 * OOS ** (i + 1)) // 2
                side_2 = 87.5 * OOS ** (i + 1)
                point_1 = (self.pos[0] + indent_1 + side_1 * j,
                           self.pos[1] + indent_1)
                point_2 = (self.pos[0] + indent_1 + side_1 * (j + 1),
                           self.pos[1] + indent_1)
                point_3 = (self.pos[0] + indent_2 + side_2 * (j + 1),
                           self.pos[1] + indent_2)
                point_4 = (self.pos[0] + indent_2 + side_2 * j,
                           self.pos[1] + indent_2)
                if self.wings[1][i][j] != '0':
                    width = 0
                else:
                    width = WIDTH
                pygame.draw.polygon(self.surface, (255, 190, 15),
                                   (point_1, point_2, point_3, point_4), width=width)

    def draw_bottom(self):
        for i in range(8):
            for j in range(8):
                move_y = 490
                indent_1 = (700 - 700 * OOS ** (8 - i)) // 2
                indent_1_y = 210 - indent_1
                side_1 = 87.5 * OOS ** (8 - i)
                indent_2 = (700 - 700 * OOS ** (7 - i)) // 2
                indent_2_y = 210 - indent_2
                side_2 = 87.5 * OOS ** (7 - i)
                point_1 = (self.pos[0] + indent_1 + side_1 * j,
                           self.pos[1] + move_y + indent_1_y)
                point_2 = (self.pos[0] + indent_1 + side_1 * (j + 1),
                           self.pos[1] + move_y + indent_1_y)
                point_3 = (self.pos[0] + indent_2 + side_2 * (j + 1),
                           self.pos[1] + move_y + indent_2_y)
                point_4 = (self.pos[0] + indent_2 + side_2 * j,
                           self.pos[1] + move_y + indent_2_y)
                if self.wings[3][7 - i][7 - j] != '0':
                    width = 0
                else:
                    width = WIDTH
                pygame.draw.polygon(self.surface, (255, 190, 15),
                                   (point_1, point_2, point_3, point_4), width=width)

    def draw_right(self):
        for j in range(8):
            for i in range(8):
                side_1 = 35 * OS ** j
                side_2 = 35 * OS ** (j + 1)
                indent_y_1 = (700 - side_1 * 8) // 2
                indent_y_2 = (700 - side_2 * 8) // 2
                indent_x_1, indent_x_2 = 210 - indent_y_1, 210 - indent_y_2
                point_1 = (self.pos[0] + 490 + indent_x_1,
                           self.pos[1] + indent_y_1 + side_1 * i)
                point_2 = (self.pos[0] + 490 + indent_x_2,
                           self.pos[1] + indent_y_2 + side_2 * i)
                point_3 = (self.pos[0] + 490 + indent_x_2,
                           self.pos[1] + indent_y_2 + side_2 * (i + 1))
                point_4 = (self.pos[0] + 490 + indent_x_1,
                           self.pos[1] + indent_y_1 + side_1 * (i + 1))
                if self.wings[2][7 - j][i] != '0':
                    width = 0
                else:
                    width = WIDTH
                pygame.draw.polygon(self.surface, (255, 190, 15),
                                    (point_1, point_2, point_3, point_4), width=width)

    def draw_left(self):
        for i in range(8):
            for j in range(8):
                move_x = 0
                indent_1 = (700 - 700 * OOS ** j) // 2
                side_1 = 87.5 * OOS ** j
                indent_2 = (700 - 700 * OOS ** (j + 1)) // 2
                side_2 = 87.5 * OOS ** (j + 1)
                point_1 = (self.pos[0] + move_x + indent_1,
                           self.pos[1] + indent_1 + side_1 * i)
                point_2 = (self.pos[0] + move_x + indent_2,
                           self.pos[1] + indent_2 + side_2 * i)
                point_3 = (self.pos[0] + move_x + indent_2,
                           self.pos[1] + indent_2 + side_2 * (i + 1))
                point_4 = (self.pos[0] + move_x + indent_1,
                           self.pos[1] + indent_1 + side_1 * (i + 1))
                if self.wings[4][j][7 - i] != '0':
                    width = 0
                else:
                    width = WIDTH
                pygame.draw.polygon(self.surface, (255, 190, 15),
                                    (point_1, point_2, point_3, point_4), width=width)
