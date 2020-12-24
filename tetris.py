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

    def make_step(self):
        if self.game == 1:
            flag = True
            currs = list()
            for i in range(20):
                for j in range(10):
                    try:
                        if self.board[i][j] == "c":
                            if i != 19:
                                if self.board[i + 1][j] == "b":
                                    flag = False
                            else:
                                flag = False
                            currs.append((i, j))
                    except IndexError:
                        print(i, j)
            for i in range(6):
                for j in range(10):
                    if self.hat[i][j] == "c":
                        self.hat[i][j] = []
                        if i == 4:
                            self.board[0][j] = 'c'
                        else:
                            self.hat[i + 1][j] = []
            currs = sorted(currs, key=lambda x: -x[0])
            if flag:
                for elem in currs:
                    self.board[elem[0]][elem[1]] = []
                    self.board[elem[0] + 1][elem[1]] = "c"
            else:
                for elem in currs:
                    self.board[elem[0]][elem[1]] = "b"
                self.new_curr()

    def new_curr(self):
        figure, self.next = self.next, random.randrange(1, 6)
        x_pos = random.randrange(0, 8)
        print(figure)
        self.hat[4][x_pos] = "c"
        if figure == 1:
            self.hat[3][x_pos] = "c"
            self.hat[2][x_pos] = "c"
            self.hat[1][x_pos] = "c"
        elif figure == 2:
            self.hat[3][x_pos] = "c"
            self.hat[4][x_pos + 1] = "c"
            self.hat[3][x_pos + 1] = "c"
        elif figure == 3:
            self.hat[4][x_pos + 1] = "c"
            self.hat[3][x_pos] = "c"
            self.hat[2][x_pos] = "c"
        elif figure == 4:
            self.hat[3][x_pos] = "c"
            self.hat[3][x_pos + 1] = "c"
            self.hat[2][x_pos] = "c"
        elif figure == 5:
            self.hat[3][x_pos] = "c"
            self.hat[3][x_pos + 1] = "c"
            self.hat[2][x_pos + 1] = "c"




    def draw_self(self):
        sprites = pygame.sprite.Group()
        for i in range(20):
            for j in range(10):
                if i >= 5:
                    pygame.draw.rect(self.surface, (255, 255, 255), (self.pos[0] + 35 * j, self.pos[1] + 35 * i, 35, 35), width=1)
                    if self.board[i][j] != []:
                        sprite = pygame.sprite.Sprite()
                        sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                                         "cube_red.png")
                        sprite.rect = sprite.image.get_rect()
                        sprite.rect.x = self.pos[0] + 35 * j
                        sprite.rect.y = self.pos[1] + 35 * i
                        sprites.add(sprite)
        sprites.draw(self.surface)

