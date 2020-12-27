import pygame
import random
import copy


# minos
# 1 - line
# 2 - cube
# 3 - g
# 4 - cross
# 5 - z
# defs
# b - blocked
# c - curr

class StupidCoderError(Exception):
    def __init__(self):
        pass


class Tetris:
    def __init__(self, screen, mode, pos):
        self.surface = screen
        self.board = [[[]] * 10 for _ in range(20)]
        self.hat = [[[]] * 10 for _ in range(6)]
        self.next = False
        self.mode = mode
        self.pos = pos
        self.game = 1
        self.next = random.randrange(1, 6)

    def rotate(self):
        if self.hat == [[[]] * 10 for _ in range(6)] and self.figure != 2:
            currs = list()
            for i in range(20):
                for j in range(10):
                    if self.board[i][j] != []:
                        if self.board[i][j][0] != '_':
                            if self.board[i][j][-1] != '_':
                                currs.append((j, i))
                            else:
                                center = (j, i)
            old_currs = copy.deepcopy(currs)
            if self.figure == 1:
                if center[1] == currs[0][1]:  # it is hori
                    currs = list()
                    currs.append((center[0], center[1] - 1))
                    currs.append((center[0], center[1] + 1))
                    currs.append((center[0], center[1] + 2))
                elif center[0] == currs[0][0]:  # it is vert
                    currs = list()
                    currs.append((center[0] - 1, center[1]))
                    currs.append((center[0] + 2, center[1]))
                    currs.append((center[0] + 1, center[1]))
                else:
                    # just why?
                    raise StupidCoderError
            if self.figure == 3:
                if (center[0] + 1, center[1] + 1) in currs and (center[0], center[1] + 1) in currs:
                    # rotation is 1. will be 2
                    currs = list()
                    currs.append((center[0] - 1, center[1]))
                    currs.append((center[0] + 1, center[1]))
                    currs.append((center[0] + 1, center[1] + 1))
                elif (center[0] + 1, center[1]) in currs and (center[0] + 1, center[1] + 1) in currs:
                    # rotation is 2. will be 3
                    currs = list()
                    currs.append((center[0], center[1] - 1))
                    currs.append((center[0], center[1] + 1))
                    currs.append((center[0] - 1, center[1] + 1))
                elif (center[0], center[1] + 1) in currs and (center[0] - 1, center[1] + 1) in currs:
                    # rotatios is 3. will be 4
                    currs = list()
                    currs.append((center[0] + 1, center[1]))
                    currs.append((center[0] - 1, center[1]))
                    currs.append((center[0] - 1, center[1] + 1))
                elif (center[0], center[1] + 1) in currs and (center[0] - 1, center[1] + 1) in currs:
                    # rotatios is 4. will be 1
                    currs = list()
                    currs.append((center[0] + 1, center[1] + 1))
                    currs.append((center[0], center[1] - 1))
                    currs.append((center[0], center[1] + 1))
                else:
                    raise StupidCoderError
            elif self.figure == 4:
                if not ((center[0], center[1] - 1) in currs):
                    # rotation is 1. will be 2
                    currs = list()
                    # currs.append((center[0] + 1, center[1]))
                    currs.append((center[0] - 1, center[1]))
                    currs.append((center[0], center[1] + 1))
                    currs.append((center[0], center[1] - 1))
                elif not ((center[0] + 1, center[1]) in currs):
                    # rotation is 2. will be 3
                    currs = list()
                    currs.append((center[0] + 1, center[1]))
                    currs.append((center[0] - 1, center[1]))
                    # currs.append((center[0], center[1] + 1))
                    currs.append((center[0], center[1] - 1))
                elif not ((center[0], center[1] + 1) in currs):
                    # rotation is 3. will be 4
                    currs = list()
                    currs.append((center[0] + 1, center[1]))
                    # currs.append((center[0] - 1, center[1]))
                    currs.append((center[0], center[1] + 1))
                    currs.append((center[0], center[1] - 1))
                elif not ((center[0] - 1, center[1]) in currs):
                    # rotation is 4. will be 1
                    currs = list()
                    currs.append((center[0] + 1, center[1]))
                    currs.append((center[0] - 1, center[1]))
                    # currs.append((center[0], center[1] + 1))
                    currs.append((center[0], center[1] - 1))
                else:
                    raise StupidCoderError
            elif self.figure == 5:
                if (center[0] - 1, center[1]) in currs and (center[0] - 1, center[1] + 1) in currs:
                    # rotation is 1. will be 2
                    currs = list()
                    currs.append((center[0] - 1, center[1]))
                    currs.append((center[0], center[1] + 1))
                    currs.append((center[0] + 1, center[1] + 1))
                elif (center[0], center[1] + 1) in currs and (center[0] + 1, center[1] + 1) in currs:
                    # rotation is 2. will be 1
                    currs = list()
                    currs.append((center[0] - 1, center[1]))
                    currs.append((center[0] - 1, center[1] - 1))
                    currs.append((center[0], center[1] + 1))
                else:
                    raise StupidCoderError
            can_rotate = True
            for elem in currs:
                if not (0 < elem[1] < 19 and 0 < elem[0] < 9):
                    can_rotate = False
                if self.board[elem[1]][elem[0]] != []:
                    if self.board[elem[1]][elem[0]][0] == '_':
                        can_rotate = False
            if can_rotate and self.figure != 2:
                for elem in old_currs:
                    color = self.board[elem[1]][elem[0]]
                    self.board[elem[1]][elem[0]] = []
                for elem in currs:
                    self.board[elem[1]][elem[0]] = color

    def catch(self, event):
        if event.key == 32:
            self.rotate()
        elif event.key in (97, 100):
            if event.key == 97:
                move = -1
            elif event.key == 100:
                move = 1
            if self.game == 1:
                can_do_step = True
                unstatic_blocks_board = []
                for i in range(20):
                    for j in range(10):
                        if self.board[i][j]:
                            if self.board[i][j][0] != "_":
                                if (j == 9 and move == 1) or (j == 0 and move == -1):
                                    can_do_step = False
                                else:
                                    try:
                                        if self.board[i][j + move][0] == '_':
                                            can_do_step = False
                                    except IndexError:
                                        pass
                                unstatic_blocks_board.append((j, i))
                unstatic_blocks_board = sorted(unstatic_blocks_board, key=lambda x: move * -int(x[0]))
                unstatic_blocks_hat = []
                for i in range(6):
                    for j in range(10):
                        if self.hat[i][j] != []:
                            if (j == 9 and move == 1) or (j == 0 and move == -1):
                                can_do_step = False
                            else:
                                unstatic_blocks_hat.append((j, i))
                unstatic_blocks_hat = sorted(unstatic_blocks_hat, key=lambda x: move * -int(x[0]))
                if can_do_step:
                    for elem in unstatic_blocks_board:
                        self.board[elem[1]][elem[0]], self.board[elem[1]][elem[0] + move] = [], self.board[elem[1]][
                            elem[0]]
                    for elem in unstatic_blocks_hat:
                        self.hat[elem[1]][elem[0]], self.hat[elem[1]][elem[0] + move] = [], self.hat[elem[1]][elem[0]]

    def make_step(self):
        if self.game == 1:
            can_do_step = True
            unstatic_blocks = []
            for i in range(20):
                for j in range(10):
                    if self.board[i][j] != []:
                        if self.board[i][j][0] != "_":
                            if i == 19:
                                can_do_step = False
                            else:
                                try:
                                    if self.board[i + 1][j][0] == '_':
                                        can_do_step = False
                                except IndexError:
                                    pass
                            unstatic_blocks.append((j, i))
                unstatic_blocks = sorted(unstatic_blocks, key=lambda x: -int(x[1]))
            if can_do_step:
                for elem in unstatic_blocks:
                    self.board[elem[1]][elem[0]], self.board[elem[1] + 1][elem[0]] = [], self.board[elem[1]][elem[0]]
            else:
                for elem in unstatic_blocks:
                    self.board[elem[1]][elem[0]] = "_" + self.board[elem[1]][elem[0]]
                self.new_curr()
            unstatic_blocks = []
            for i in range(6):
                for j in range(10):
                    if self.hat[i][j] != []:
                        if i != 5:
                            unstatic_blocks.append((j, i))
                        else:
                            try:
                                if self.hat[i][j][0] != '_':
                                    self.hat[i][j], self.board[i][j] = [], self.hat[i][j]
                                # else: game over
                            except IndexError:
                                print(self.board[i][j])
            unstatic_blocks = sorted(unstatic_blocks, key=lambda x: -int(x[1]))
            for elem in unstatic_blocks:
                self.hat[elem[1]][elem[0]], self.hat[elem[1] + 1][elem[0]] = [], self.hat[elem[1]][elem[0]]

    def new_curr(self):
        figure, self.next, x_pos = self.next, random.randrange(1, 6), random.randrange(0, 8)
        color = random.choice(['1', '2', '3'])
        self.hat[4][x_pos] = color
        if figure == 1:
            self.hat[3][x_pos] = color
            self.hat[2][x_pos] = color + '_'
            self.hat[1][x_pos] = color
        elif figure == 2:
            self.hat[3][x_pos] = color
            self.hat[4][x_pos + 1] = color
            self.hat[3][x_pos + 1] = color
        elif figure == 3:
            self.hat[4][x_pos + 1] = color
            self.hat[3][x_pos] = color + "_"
            self.hat[2][x_pos] = color
        elif figure == 4:
            self.hat[3][x_pos] = color + "_"
            self.hat[3][x_pos + 1] = color
            self.hat[2][x_pos] = color
        elif figure == 5:
            self.hat[3][x_pos] = color
            self.hat[3][x_pos + 1] = color + '_'
            self.hat[2][x_pos + 1] = color
        self.figure = figure

    def draw_self(self):
        sprites = pygame.sprite.Group()
        for i in range(20):
            for j in range(10):
                if i >= 5:
                    pygame.draw.rect(self.surface, (255, 255, 255),
                                     (self.pos[0] + 35 * j, self.pos[1] + 35 * i, 35, 35), width=1)
                    if self.board[i][j] != []:
                        sprite = pygame.sprite.Sprite()
                        if self.board[i][j][0] == "_" and self.board[i][j][-1] == "_":
                            color = self.board[i][j][1:-1]
                        elif self.board[i][j][0] == "_":
                            color = self.board[i][j][1:]
                        elif self.board[i][j][-1] == "_":
                            color = self.board[i][j][:-1]
                        else:
                            color = self.board[i][j]
                        sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                                         f"cube_{color}.png")
                        sprite.rect = sprite.image.get_rect()
                        sprite.rect.x = self.pos[0] + 35 * j
                        sprite.rect.y = self.pos[1] + 35 * i
                        sprites.add(sprite)
        sprites.draw(self.surface)
