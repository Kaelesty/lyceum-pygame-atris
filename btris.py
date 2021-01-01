import pygame
import random

# minos
# 1 - line
# 2 - cube
# 3 - g
# 4 - cross
# 5 - z


class Bmino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                       "cube_-1.png")
        self.rect = self.image.get_rect()


class Btris:
    def __init__(self, surface, size, pos):
        self.surface = surface
        self.size = int(size)
        self.board = self.board = [[[]] * int(size) for _ in range(int(size))]
        self.pos = pos
        self.figures = [[random.choice([1, 2, 3, 4, 5]), (self.pos[0] + 800 + 70, self.pos[1] + 105), 1],
                        [random.choice([1, 2, 3, 4, 5]), (self.pos[0] + 800 + 70, self.pos[1] + 105 + 245), 1],
                        [random.choice([1, 2, 3, 4, 5]), (self.pos[0] + 800 + 70, self.pos[1] + 105 + 490), 1]]
        self.following = 0

    def update(self, pos):
        if self.following != 0:
            self.figures[self.following - 1][1] = pos

    def catch_mbu(self, pos):
        if self.pos[0] <= pos[0] <= self.pos[0] + 35 * self.size:
            if self.pos[1] <= pos[1] <= self.pos[1] + 35 * self.size:
                coords = list()
                i, j = pos[1] // 35, pos[0] // 35
                coords.append((j, i))
                if self.figures[self.following - 1][0] == 1:
                    if self.figures[self.following - 1][2] == 1:
                        x_move = 1
                        y_move = 0
                    else:
                        x_move = 0
                        y_move = 1
                    coords.append((j + x_move, i + y_move))
                    coords.append((j + x_move * 2, i + y_move * 2))
                    coords.append((j - x_move, i - y_move))
                elif self.figures[self.following - 1][0] == 2:
                    coords.append((j + 1, i))
                    coords.append((j + 1, i + 1))
                    coords.append((j, i + 1))
                elif self.figures[self.following - 1][0] == 3:
                    if self.figures[self.following - 1][2] == 1:
                        coords.append((j, i - 1))
                        coords.append((j + 1, i - 1))
                        coords.append((j, i + 1))
                    elif self.figures[self.following - 1][2] == 2:
                        coords.append((j - 1, i))
                        coords.append((j + 1, i))
                        coords.append((j + 1, i + 1))
                    elif self.figures[self.following - 1][2] == 3:
                        coords.append((j, i - 1))
                        coords.append((j, i + 1))
                        coords.append((j - 1, i + 1))
                    elif self.figures[self.following - 1][2] == 4:
                        coords.append((j - 1, i))
                        coords.append((j + 1, i))
                        coords.append((j - 1, i - 1))
                elif self.figures[self.following - 1][0] == 4:
                    if self.figures[self.following - 1][2] == 1:
                        # coords.append((j, i - 1))
                        coords.append((j, i + 1))
                        coords.append((j + 1, i))
                        coords.append((j - 1, i))
                    elif self.figures[self.following - 1][2] == 2:
                        coords.append((j, i - 1))
                        coords.append((j, i + 1))
                        # coords.append((j + 1, i))
                        coords.append((j - 1, i))
                    elif self.figures[self.following - 1][2] == 3:
                        coords.append((j, i - 1))
                        # coords.append((j, i + 1))
                        coords.append((j + 1, i))
                        coords.append((j - 1, i))
                    elif self.figures[self.following - 1][2] == 4:
                        coords.append((j, i - 1))
                        coords.append((j, i + 1))
                        coords.append((j + 1, i))
                        # coords.append((j - 1, i))
                elif self.figures[self.following - 1][0] == 5:
                    if self.figures[self.following - 1][2] == 1:
                        coords.append((j, i - 1))
                        coords.append((j + 1, i - 1))
                        coords.append((j - 1, i))
                    else:
                        coords.append((j - 1, i))
                        coords.append((j - 1, i - 1))
                        coords.append((j, i + 1))
                can_set = True
                for elem in coords:
                    if 0 <= elem[1] < 20 and 0 <= elem[0] < 20:
                        if self.board[elem[1]][elem[0]]:
                            can_set = False
                            break
                    else:
                        can_set = False
                        break
                if can_set:
                    for elem in coords:
                        self.board[elem[1]][elem[0]] = 1
                    self.figures[self.following - 1] = [random.choice([1, 2, 3, 4, 5]),
                                                        (self.pos[0] + 800 + 70,
                                                         self.pos[1] + 105 + 245 * (self.following - 1)), 1]
                    self.check_fulls()
                else:
                    self.stop_following()
            else:
                self.stop_following()
        else:
            self.stop_following()

    def catch(self, event):
        if event.key == 32 and self.following != 0:
            print(self.figures[self.following - 1][2])
            if self.figures[self.following - 1][0] in (3, 4):
                self.figures[self.following - 1][2] += 1
                if self.figures[self.following - 1][2] == 5:
                    self.figures[self.following - 1][2] = 1
            elif self.figures[self.following - 1][0] in (1, 5):
                self.figures[self.following - 1][2] += 1
                if self.figures[self.following - 1][2] == 3:
                    self.figures[self.following - 1][2] = 1

    def check_fulls(self):
        for j in range(self.size):
            if self.board[j] == [1] * self.size:
                self.board[j] = [[]] * self.size
            else:
                flag = True
                for i in range(self.size):
                    if self.board[i][j] == 1:
                        if self.board[i][j] != self.board[0][j]:
                            flag = False
                    else:
                        flag = False
                        break
                if flag:
                    for i in range(self.size):
                        self.board[i][j] = []

    def stop_following(self):
        self.figures[self.following - 1][1] = (self.pos[0] + 800 + 70, self.pos[1] + 105 + 245 * (self.following - 1))
        self.following = 0

    def draw_self(self):
        blocks = pygame.sprite.Group()
        for i in range(self.size):
            for j in range(self.size):
                pygame.draw.rect(self.surface, (255, 190, 15),
                                 (self.pos[0] + 35 * j, self.pos[1] + 35 * i, 35, 35), width=1)
                if self.board[i][j] == 1:
                    sprite = pygame.sprite.Sprite()
                    sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                                     "cube_-1.png")
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.x = self.pos[0] + 35 * j
                    sprite.rect.y = self.pos[1] + 35 * i
                    blocks.add(sprite)
        blocks.draw(self.surface)
        self.draw_fields()
        self.draw_figures()

    def draw_fields(self):
        for i in range(6):
            for j in range(6):
                pygame.draw.rect(self.surface, (255, 255, 255),
                                (self.pos[0] + 800 + 35 * j, self.pos[1] + 35 * i, 35, 35), width=1)

                pygame.draw.rect(self.surface, (255, 255, 255),
                                 (self.pos[0] + 800 + 35 * j, self.pos[1] + 35 * i + 245, 35, 35), width=1)

                pygame.draw.rect(self.surface, (255, 255, 255),
                                 (self.pos[0] + 800 + 35 * j, self.pos[1] + 35 * i + 490, 35, 35), width=1)

    def draw_figures(self):
        figures = pygame.sprite.Group()
        for i in range(3):
            if self.figures[i][0] == 1:
                if self.figures[i][2] == 1:
                    x_move = 35
                    y_move = 0
                else:
                    y_move = 35
                    x_move = 0
                sprite1 = Bmino()
                sprite1.rect.x = self.figures[i][1][0]
                sprite1.rect.y = self.figures[i][1][1]
                figures.add(sprite1)
                sprite1 = Bmino()
                sprite1.rect.x = self.figures[i][1][0] - x_move
                sprite1.rect.y = self.figures[i][1][1] - y_move
                figures.add(sprite1)
                sprite1 = Bmino()
                sprite1.rect.x = self.figures[i][1][0] + x_move
                sprite1.rect.y = self.figures[i][1][1] + y_move
                figures.add(sprite1)
                sprite1 = Bmino()
                sprite1.rect.x = self.figures[i][1][0] + x_move * 2
                sprite1.rect.y = self.figures[i][1][1] + y_move * 2
                figures.add(sprite1)
            elif self.figures[i][0] == 2:
                sprite1 = Bmino()
                sprite1.rect.x = self.figures[i][1][0]
                sprite1.rect.y = self.figures[i][1][1]
                figures.add(sprite1)
                sprite1 = Bmino()
                sprite1.rect.x = self.figures[i][1][0] + 35
                sprite1.rect.y = self.figures[i][1][1]
                figures.add(sprite1)
                sprite1 = Bmino()
                sprite1.rect.x = self.figures[i][1][0]
                sprite1.rect.y = self.figures[i][1][1] + 35
                figures.add(sprite1)
                sprite1 = Bmino()
                sprite1.rect.x = self.figures[i][1][0] + 35
                sprite1.rect.y = self.figures[i][1][1] + 35
                figures.add(sprite1)
            elif self.figures[i][0] == 3:
                if self.figures[i][2] == 1:
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0] + 35
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] + 35
                    figures.add(sprite1)
                elif self.figures[i][2] == 2:
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0] - 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0] + 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0] + 35
                    sprite1.rect.y = self.figures[i][1][1] + 35
                    figures.add(sprite1)
                elif self.figures[i][2] == 3:
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] + 35
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0] - 35
                    sprite1.rect.y = self.figures[i][1][1] + 35
                    figures.add(sprite1)
                elif self.figures[i][2] == 4:
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0] + 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0] - 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0] - 35
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
            elif self.figures[i][0] == 4:
                sprite1 = Bmino()
                sprite1.rect.x = self.figures[i][1][0]
                sprite1.rect.y = self.figures[i][1][1]
                figures.add(sprite1)
                if self.figures[i][2] == 1:
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0] + 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0] - 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] + 35
                    figures.add(sprite1)
                elif self.figures[i][2] == 2:
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0] - 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] + 35
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
                elif self.figures[i][2] == 3:
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0] + 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0] - 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
                elif self.figures[i][2] == 4:
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0] + 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] + 35
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
            elif self.figures[i][0] == 5:
                sprite1 = Bmino()
                sprite1.rect.x = self.figures[i][1][0]
                sprite1.rect.y = self.figures[i][1][1]
                figures.add(sprite1)
                sprite1 = Bmino()
                sprite1.rect.x = self.figures[i][1][0] - 35
                sprite1.rect.y = self.figures[i][1][1]
                figures.add(sprite1)
                if self.figures[i][2] == 2:
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0] - 35
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] + 35
                    figures.add(sprite1)
                elif self.figures[i][2] == 1:
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
                    sprite1 = Bmino()
                    sprite1.rect.x = self.figures[i][1][0] + 35
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
        figures.draw(self.surface)

    def catch_mbd(self, pos):
        if self.pos[0] + 800 <= pos[0] <= self.pos[0] + 800 + 35 * 6:
            if self.pos[1] <= pos[1] <= self.pos[1] + 35 * 6:
                self.following = 1
                return True
            elif self.pos[1] <= pos[1] - 245 <= self.pos[1] + 35 * 6:
                self.following = 2
                return True
            elif self.pos[1] <= pos[1] - 490 <= self.pos[1] + 35 * 6:
                self.following = 3
                return True
        return False
