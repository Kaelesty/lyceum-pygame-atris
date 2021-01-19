import pygame
import random

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

    def new_current(self):
        self.current_wing = random.choice([1, 2, 3, 4])
        color = random.choice(['1', '2', '3'])
        figure = random.randrange(1, 6)
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
            self.hat[0][x + 1] = color
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
        #  check wing possible
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
                print(' ')
                print(i)
                print(j)
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

    def game_over(self):
        pass

    def catch(self, event): # A - 97, D - 100
        if event.key == 97:
            #  check wing possible
            _can = True
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
        if event.key == 100:
            #  check wing possible
            _can = True
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



    def draw_self(self):
        pygame.draw.rect(self.surface, (255, 190, 15),
                         (self.pos[0], self.pos[1], 700, 700), width=WIDTH)
        self.draw_center()
        self.draw_top()
        self.draw_bottom()
        self.draw_left()
        self.draw_right()

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
