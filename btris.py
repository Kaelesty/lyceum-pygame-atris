import pygame
import random
import sqlite3


# minos
# 1 - line
# 2 - cube
# 3 - g
# 4 - cross
# 5 - z

WIDTH = 5


class Bmino(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                       f"cube_{color}.png")
        self.rect = self.image.get_rect()


class Btris:
    def __init__(self, surface, size, pos):
        self.surface = surface
        self.size = int(size)
        self.board = self.board = [[[]] * int(size) for _ in range(int(size))]
        self.pos = pos
        self.figures = [[random.choice([1, 2, 3, 4, 5]),
                         (self.pos[0] + 800 + 70, self.pos[1] + 105), 1, random.choice([1, 2, 3])],
                        [random.choice([1, 2, 3, 4, 5]),
                         (self.pos[0] + 800 + 70, self.pos[1] + 105 + 245), 1, random.choice([1, 2, 3])],
                        [random.choice([1, 2, 3, 4, 5]),
                         (self.pos[0] + 800 + 70, self.pos[1] + 105 + 490), 1, random.choice([1, 2, 3])]]
        # figure: [form, (pos_x, pos_y), rotation#(2 for 1 and 5 forms;1 for 2 form;4 for 3 and 4 forms)#, color]
        self.following = 0
        self.score = 0
        self.particles_target = (self.pos[0] + 1120, self.pos[1] + 10)
        self.particles = pygame.sprite.Group()
        self.particles_spawn = 0

    def generate_particles(self, height=-1, longtude=-1):
        self.particles_spawn = 100
        for i in range(self.size):
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                              "particle.png")
            sprite.rect = sprite.image.get_rect()
            if height != -1:
                sprite.rect.x = self.pos[0] + 15 + 35 * i
                sprite.rect.y = self.pos[1] + 15 + 35 * height
            else:
                sprite.rect.x = self.pos[0] + 15 + 35 * longtude
                sprite.rect.y = self.pos[1] + 15 + 35 * i
            self.particles.add(sprite)

    def update_particles(self):
        new_particles = []
        if self.particles_spawn < -200:
            for elem in list(self.particles):
                self.score += 1
            self.particles = pygame.sprite.Group()
        else:
            for elem in list(self.particles):
                self.particles_spawn -= 1
                if self.particles_spawn <= 0:
                    _add = True
                    if elem.rect.x > self.particles_target[0]:
                        elem.rect.x -= 16
                        if elem.rect.x < self.particles_target[0]:
                            self.score += 1
                            _add = False
                    elif elem.rect.x < self.particles_target[0]:
                        elem.rect.x += 16
                        if elem.rect.x > self.particles_target[0]:
                            self.score += 1
                            _add = False
                    if elem.rect.y > self.particles_target[1]:
                        elem.rect.y -= 2
                        if elem.rect.y < self.particles_target[1]:
                            self.score += 1
                            _add = False
                    elif elem.rect.y < self.particles_target[1]:
                        elem.rect.y += 2
                        if elem.rect.y > self.particles_target[1]:
                            self.score += 1
                            _add = False
                    if _add:
                        new_particles.append(elem)
                else:
                    elem.rect.x += random.randrange(-2, 2)
                    elem.rect.y += random.randrange(-2, 2)
                    new_particles.append(elem)
            self.particles = pygame.sprite.Group()
            for elem in new_particles:
                if (elem.rect.x, elem.rect.y) != self.particles_target:
                    self.particles.add(elem)
                else:
                    self.score += 1

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
                    if 0 <= elem[1] < self.size and 0 <= elem[0] < self.size:
                        if self.board[elem[1]][elem[0]]:
                            can_set = False
                            break
                    else:
                        can_set = False
                        break
                if can_set:
                    for elem in coords:
                        self.board[elem[1]][elem[0]] = self.figures[self.following - 1][-1]
                    self.figures[self.following - 1] = [random.choice([1, 2, 3, 4, 5]),
                                                        (self.pos[0] + 800 + 70,
                                                         self.pos[1] + 105 + 245 * (self.following - 1)), 1,
                                                        random.choice([1, 2, 3])]
                    self.check_fulls()
                else:
                    self.stop_following()
            else:
                self.stop_following()
        else:
            self.stop_following()

    def catch(self, event):
        if event.key == 32 and self.following != 0:
            if self.figures[self.following - 1][0] in (3, 4):
                self.figures[self.following - 1][2] += 1
                if self.figures[self.following - 1][2] == 5:
                    self.figures[self.following - 1][2] = 1
            elif self.figures[self.following - 1][0] in (1, 5):
                self.figures[self.following - 1][2] += 1
                if self.figures[self.following - 1][2] == 3:
                    self.figures[self.following - 1][2] = 1

    def check_fulls(self):
        for i in range(self.size):
            _full_hor = True
            _full_vert = True
            for j in range(self.size):
                if not self.board[i][j]:
                    _full_hor = False
                if not self.board[j][i]:
                    _full_vert = False
            if _full_hor:
                self.board[i] = [[]] * self.size
                self.generate_particles(height=i)
            if _full_vert:
                for j in range(self.size):
                    self.board[j][i] = []
                self.generate_particles(longtude=i)

    def stop_following(self):
        self.figures[self.following - 1][1] = (self.pos[0] + 800 + 70, self.pos[1] + 105 + 245 * (self.following - 1))
        self.following = 0

    def terminate(self):
        con = sqlite3.connect("Data\ "[0:-1] + "AData.sqlite")
        cur = con.cursor()
        data = cur.execute(f"SELECT Btris_{self.size} FROM Scores").fetchall()
        if list(data)[0][0] < self.score:
            cur.execute(f"UPDATE Scores SET Btris_{self.size} = {self.score}")
        con.commit()
        con.close()
        # i will be back

    def draw_score(self):
        font = pygame.font.Font("Data\ "[0:-1] + "Konstanting.ttf", 50)
        text = font.render("Score:", True, (255, 190, 15))
        text_x = self.pos[0] + 1110
        text_y = self.pos[1]
        text_w = text.get_width()
        text_h = text.get_height()
        self.surface.blit(text, (text_x, text_y))
        text = font.render(str(self.score), True, (255, 190, 15))
        text_x = self.pos[0] + 1110
        text_y = self.pos[1] + 50
        text_w = text.get_width()
        text_h = text.get_height()
        self.surface.blit(text, (text_x, text_y))

    def draw_self(self):
        blocks = pygame.sprite.Group()
        for i in range(self.size):
            for j in range(self.size):
                pygame.draw.rect(self.surface, (255, 190, 15),
                                 (self.pos[0] + 35 * j, self.pos[1] + 35 * i, 35, 35), width=1)
                if self.board[i][j]:
                    sprite = pygame.sprite.Sprite()
                    sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                                     f"cube_{self.board[i][j]}.png")
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.x = self.pos[0] + 35 * j
                    sprite.rect.y = self.pos[1] + 35 * i
                    blocks.add(sprite)
        blocks.draw(self.surface)
        self.draw_fields()
        self.draw_figures()
        self.draw_score()
        sprites = pygame.sprite.Group()
        sprite1 = pygame.sprite.Sprite()
        sprite1.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                          "press_x.png")
        sprite1.rect = sprite1.image.get_rect()
        sprite1.rect.x = self.pos[0] + 1030
        sprite1.rect.y = self.pos[1] + 675
        sprites.add(sprite1)
        sprites.draw(self.surface)
        self.particles.draw(self.surface)

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
                sprite1 = Bmino(self.figures[i][-1])
                sprite1.rect.x = self.figures[i][1][0]
                sprite1.rect.y = self.figures[i][1][1]
                figures.add(sprite1)
                sprite1 = Bmino(self.figures[i][-1])
                sprite1.rect.x = self.figures[i][1][0] - x_move
                sprite1.rect.y = self.figures[i][1][1] - y_move
                figures.add(sprite1)
                sprite1 = Bmino(self.figures[i][-1])
                sprite1.rect.x = self.figures[i][1][0] + x_move
                sprite1.rect.y = self.figures[i][1][1] + y_move
                figures.add(sprite1)
                sprite1 = Bmino(self.figures[i][-1])
                sprite1.rect.x = self.figures[i][1][0] + x_move * 2
                sprite1.rect.y = self.figures[i][1][1] + y_move * 2
                figures.add(sprite1)
            elif self.figures[i][0] == 2:
                sprite1 = Bmino(self.figures[i][-1])
                sprite1.rect.x = self.figures[i][1][0]
                sprite1.rect.y = self.figures[i][1][1]
                figures.add(sprite1)
                sprite1 = Bmino(self.figures[i][-1])
                sprite1.rect.x = self.figures[i][1][0] + 35
                sprite1.rect.y = self.figures[i][1][1]
                figures.add(sprite1)
                sprite1 = Bmino(self.figures[i][-1])
                sprite1.rect.x = self.figures[i][1][0]
                sprite1.rect.y = self.figures[i][1][1] + 35
                figures.add(sprite1)
                sprite1 = Bmino(self.figures[i][-1])
                sprite1.rect.x = self.figures[i][1][0] + 35
                sprite1.rect.y = self.figures[i][1][1] + 35
                figures.add(sprite1)
            elif self.figures[i][0] == 3:
                if self.figures[i][2] == 1:
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0] + 35
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] + 35
                    figures.add(sprite1)
                elif self.figures[i][2] == 2:
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0] - 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0] + 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0] + 35
                    sprite1.rect.y = self.figures[i][1][1] + 35
                    figures.add(sprite1)
                elif self.figures[i][2] == 3:
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] + 35
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0] - 35
                    sprite1.rect.y = self.figures[i][1][1] + 35
                    figures.add(sprite1)
                elif self.figures[i][2] == 4:
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0] + 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0] - 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0] - 35
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
            elif self.figures[i][0] == 4:
                sprite1 = Bmino(self.figures[i][-1])
                sprite1.rect.x = self.figures[i][1][0]
                sprite1.rect.y = self.figures[i][1][1]
                figures.add(sprite1)
                if self.figures[i][2] == 1:
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0] + 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0] - 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] + 35
                    figures.add(sprite1)
                elif self.figures[i][2] == 2:
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0] - 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] + 35
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
                elif self.figures[i][2] == 3:
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0] + 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0] - 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
                elif self.figures[i][2] == 4:
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0] + 35
                    sprite1.rect.y = self.figures[i][1][1]
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] + 35
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
            elif self.figures[i][0] == 5:
                sprite1 = Bmino(self.figures[i][-1])
                sprite1.rect.x = self.figures[i][1][0]
                sprite1.rect.y = self.figures[i][1][1]
                figures.add(sprite1)
                sprite1 = Bmino(self.figures[i][-1])
                sprite1.rect.x = self.figures[i][1][0] - 35
                sprite1.rect.y = self.figures[i][1][1]
                figures.add(sprite1)
                if self.figures[i][2] == 2:
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0] - 35
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] + 35
                    figures.add(sprite1)
                elif self.figures[i][2] == 1:
                    sprite1 = Bmino(self.figures[i][-1])
                    sprite1.rect.x = self.figures[i][1][0]
                    sprite1.rect.y = self.figures[i][1][1] - 35
                    figures.add(sprite1)
                    sprite1 = Bmino(self.figures[i][-1])
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
