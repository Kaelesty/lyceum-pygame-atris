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
        if mode == 'classic':
            self.board = [[[]] * 10 for _ in range(20)]
            self.next = False
        self.pos = pos
        self.spawn_curr()

    def spawn_curr(self):
        if self.next is False:
            curr = random.choice([1, 2, 3, 4, 5])
        else:
            curr = self.next
        self.next = random.choice([1, 2, 3, 4, 5])
        curr_y = -4
        if curr == 1:
            curr_x = random.randrange(1, 11)
        elif curr in (2, 3, 5, 4):
            curr_x = random.randrange(1, 10)
        if curr == 1:
            self.curr = [[curr_x, curr_y], [curr_x, curr_y + 1], [curr_x, curr_y + 2], [curr_x, curr_y + 3]]
        elif curr == 2:
            self.curr = [[curr_x, curr_y], [curr_x, curr_y + 1], [curr_x + 1, curr_y + 1], [curr_x + 1, curr_y]]
        elif curr == 3:
            self.curr = [[curr_x, curr_y], [curr_x, curr_y + 1], [curr_x, curr_y + 2], [curr_x + 1, curr_y + 2]]
        elif curr == 4:
            self.curr = [[curr_x, curr_y], [curr_x + 1, curr_y + 1], [curr_x + 1, curr_y], [curr_x + 2, curr_y]]
        elif curr == 5:
            self.curr = [[curr_x, curr_y], [curr_x, curr_y + 1], [curr_x + 1, curr_y + 1], [curr_x + 1, curr_y + 2]]

    def make_step(self):
        flag = True
        for i in range(len(self.curr)):
            if self.curr[i][1] >= 0:
                if self.curr[i][1] < 19:
                    print(self.curr[i])
                    if self.board[self.curr[i][1] + 1][self.curr[i][0]] == "b":
                        flag = False
                        break
                else:
                    flag = False
                    break
        if not flag:
            self.stop_curr()
        else:
            for elem in self.curr:
                self.curr[i][1] = self.curr[i][1] + 1

    def stop_curr(self):
        for elem in self.curr:
            self.board[elem[1]][elem[0]] = "b"
        self.spawn_curr()

    def draw_self(self):
        sprites = pygame.sprite.Group()
        for i in range(20):
            for j in range(10):
                print(self.board)
                pygame.draw.rect(self.surface, (255, 255, 255), (self.pos[0] + 35 * j, self.pos[1] + 35 * i, 35, 35), width=1)
                if self.board[i][j] != []:
                    sprite = pygame.sprite.Sprite()
                    sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                                     "cube_red.png")
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.x = self.pos[0] + 35 * j
                    sprite.rect.y = self.pos[1] + 35 * i
                    sprites.add(sprite)
                elif [j, i] in self.curr:
                    sprite = pygame.sprite.Sprite()
                    sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                                     "cube_red.png")
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.x = self.pos[0] + 35 * j
                    sprite.rect.y = self.pos[1] + 35 * i
                    sprites.add(sprite)
        sprites.draw(self.surface)

