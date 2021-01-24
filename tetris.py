import pygame
import random
import copy
import sqlite3
import datetime as dt

# GAME MODES:
# easy : показывается след. фигура, можно вращать фигуры на паузе
# normal : нельзя вращать фигуры на паузе
# hard : след. фигура не показывается

# minos
# 1 - line
# 2 - cube
# 3 - g
# 4 - cross
# 5 - z

WIDTH = 1



class StupidCoderError(Exception):
    def __init__(self):
        pass


class Tetris:
    def __init__(self, screen, mode, pos):
        self.surface = screen
        self.board = [[[]] * 10 for _ in range(20)]
        self.board[19] = ["_2"] * 10
        self.hat = [[[]] * 10 for _ in range(6)]
        self.mode = mode
        self.pos = pos
        self.game = 1
        self.next = random.randrange(1, 6)
        self.score = 0
        self.secondary_pos = (self.pos[0] + 350, self.pos[1])
        self.pause = 0.9
        self.begin = dt.datetime.now()
        self.particles = pygame.sprite.Group()
        self.particles_target = (self.pos[0] + 350 + 160, self.pos[1] + 310 + 50)
        self.particles_spawn = 0

    def terminate(self):
        con = sqlite3.connect("Data\ "[0:-1] + "AData.sqlite")
        cur = con.cursor()
        data = cur.execute(f"SELECT Classic_{self.mode} FROM Scores").fetchall()
        if list(data)[0][0] < self.score:
            cur.execute(f"UPDATE Scores SET Classic_{self.mode} = {self.score}")
        con.commit()
        con.close()
        # i will be back

    def check_full_lines(self):
        returned = []
        for i in range(20):
            flag = True
            for j in range(10):
                if self.board[i][j] != []:
                    if self.board[i][j][0] != '_':
                        flag = False
                else:
                    flag = False
            if flag:
                returned.append(i)
        return returned

    def rotate(self):
        if self.game == 1 or self.mode == "classic":
            try:
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
                            currs.append((center[0] - 1, center[1] - 1))
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
                            currs.append((center[0], center[1] + 1))
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
                            print(center)
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
            except Exception:
                pass

    def catch(self, event):
        if event.key == 27:
            if self.game == 0:
                self.game = 1
            else:
                self.game = 0
        elif event.key == 32:
            self.rotate()
        elif event.key == 120:
            self.terminate()
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

    def draw_score(self):
        pygame.draw.rect(self.surface, (255, 190, 15),
                         (self.pos[0] + 350, self.pos[1] + 310, 320, 100), width=WIDTH)
        font = pygame.font.Font("Data\ "[0:-1] + "Konstanting.ttf", 50)
        text = font.render("Score:", True, (255, 190, 15))
        text_x = self.pos[0] + 350
        text_y = self.pos[1] + 310
        text_w = text.get_width()
        text_h = text.get_height()
        self.surface.blit(text, (text_x, text_y))
        text = font.render(str(self.score), True, (255, 190, 15))
        text_x = self.pos[0] + 350
        text_y = self.pos[1] + 350
        text_w = text.get_width()
        text_h = text.get_height()
        self.surface.blit(text, (text_x, text_y))

    def check_game_over(self):
        for i in range(8):
            if self.board[0][i] != []:
                if self.board[0][i][0] == "_":
                    self.game = 2


    def generate_particles(self, height):
        self.particles_spawn = 100
        for i in range(10):
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                              "particle.png")
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = self.pos[0] + 15 + 35 * i
            sprite.rect.y = self.pos[1] + 15 + 35 * height
            self.particles.add(sprite)

    def update_particles(self):
        new_particles = []
        for elem in list(self.particles):
            if self.particles_spawn <= 0:
                _add = True
                if elem.rect.x > self.particles_target[0]:
                    elem.rect.x -= 8
                    if elem.rect.x < self.particles_target[0]:
                        self.score += 1
                        _add = False
                elif elem.rect.x < self.particles_target[0]:
                    elem.rect.x += 8
                    if elem.rect.x > self.particles_target[0]:
                        self.score += 1
                        _add = False
                if elem.rect.y > self.particles_target[1]:
                    elem.rect.y -= 8
                    if elem.rect.y < self.particles_target[1]:
                        self.score += 1
                        _add = False
                elif elem.rect.y < self.particles_target[1]:
                    elem.rect.y += 8
                    if elem.rect.y > self.particles_target[1]:
                        self.score += 1
                        _add = False
                if _add:
                    new_particles.append(elem)
            else:
                self.particles_spawn -= 1
                elem.rect.x += random.randrange(-2, 2)
                elem.rect.y += random.randrange(-2, 2)
                new_particles.append(elem)
        self.particles = pygame.sprite.Group()
        for elem in new_particles:
            if (elem.rect.x, elem.rect.y) != self.particles_target:
                self.particles.add(elem)
            else:
                self.score += 1


    def make_step(self):
        now = dt.datetime.now()
        self.check_game_over()
        self.update_particles()
        if self.game == 1 and (now - self.begin).total_seconds() >= self.pause:
            self.begin = now
            if self.pause > 0:
                self.pause -= 0.002
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
                                    self.hat[i][j], self.board[0][j] = [], self.hat[i][j]
                                # else: game over
                            except IndexError:
                                print(self.board[i][j])
            unstatic_blocks = sorted(unstatic_blocks, key=lambda x: -int(x[1]))
            for elem in unstatic_blocks:
                self.hat[elem[1]][elem[0]], self.hat[elem[1] + 1][elem[0]] = [], self.hat[elem[1]][elem[0]]
            for elem in self.check_full_lines():
                self.generate_particles(elem)
                for i in range(elem, 0, -1):
                    self.board[i] = copy.deepcopy(self.board)[i - 1]

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
            self.hat[2][x_pos - 1] = color
            self.hat[3][x_pos - 1] = color
            self.hat[3][x_pos] = color + "_"
        self.figure = figure

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
                    pygame.draw.rect(self.surface, (255, 255, 255),
                                     (self.pos[0] + 350 + 35 * j, self.pos[1] + 35 * i, 35, 35), width=1)
                    if (i, j) in coords:
                        sprite = pygame.sprite.Sprite()
                        sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                                         "cube_-1.png")
                        sprite.rect = sprite.image.get_rect()
                        sprite.rect.x = self.pos[0] + 350 + 35 * j
                        sprite.rect.y = self.pos[1] + 35 * i
                        sprites.add(sprite)
            sprites.draw(self.surface)

    def draw_self(self):
        sprites = pygame.sprite.Group()
        for i in range(20):
            for j in range(10):
                if True:
                    pygame.draw.rect(self.surface, (255, 190, 15),
                                     (self.pos[0] + 35 * j, self.pos[1] + 35 * i, 35, 35), width=1)
                    if self.board[i][j]:
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
        if self.game == 0:
            sprite1 = pygame.sprite.Sprite()
            sprite1.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                              "press_x.png")
            sprite1.rect = sprite.image.get_rect()
            sprite1.rect.x = self.pos[0] + 60
            sprite1.rect.y = self.pos[1] + 490
            sprites.add(sprite1)
        pygame.draw.rect(self.surface, (255, 190, 15),
                         (self.pos[0] + 350, self.pos[1] + 210, 320, 100), width=WIDTH)
        sprite1 = pygame.sprite.Sprite()
        sprite1.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                          "status.png")
        sprite1.rect = sprite1.image.get_rect()
        sprite1.rect.x = self.pos[0] + 350
        sprite1.rect.y = self.pos[1] + 215
        sprites.add(sprite1)
        if self.game == 0:
            sprite1 = pygame.sprite.Sprite()
            sprite1.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                              "paused.png")
            sprite1.rect = sprite1.image.get_rect()
            sprite1.rect.x = self.pos[0] + 360
            sprite1.rect.y = self.pos[1] + 215
            sprites.add(sprite1)
        elif self.game == 2:
            sprite1 = pygame.sprite.Sprite()
            sprite1.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                              "game_over.png")
            sprite1.rect = sprite1.image.get_rect()
            sprite1.rect.x = self.pos[0] + 360
            sprite1.rect.y = self.pos[1] + 215
            sprites.add(sprite1)
        else:
            sprite1 = pygame.sprite.Sprite()
            sprite1.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                              "gim.png")
            sprite1.rect = sprite1.image.get_rect()
            sprite1.rect.x = self.pos[0] + 360
            sprite1.rect.y = self.pos[1] + 215
            sprites.add(sprite1)
        sprites.draw(self.surface)
        self.draw_secondary()
        sprites.draw(self.surface)
        self.draw_score()
        self.particles.draw(self.surface)
