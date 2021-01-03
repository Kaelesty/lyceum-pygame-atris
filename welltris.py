import pygame
import random

OS = 1 / 0.8917795292374964
OOS = 0.8917795292374964
WIDTH = 4


class Welltris:
    def __init__(self, screen, mode, pos):
        self.surface = screen
        self.top = [[[]] * 8 for _ in range(8)]
        self.bottom = [[[]] * 8 for _ in range(8)]
        self.right = [[[]] * 8 for _ in range(8)]
        self.left = [[[]] * 8 for _ in range(8)]
        self.mode = mode
        self.pos = pos
        self.game = 1
        self.next = random.randrange(1, 6)
        self.score = 0

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
                pygame.draw.rect(self.surface, (255, 190, 15),
                                 (self.pos[0] + 210 + 35 * j, self.pos[1] + 210 + 35 * i, 35, 35), width=WIDTH)

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
                pygame.draw.polygon(self.surface, (255, 190, 15),
                                   (point_1, point_2, point_3, point_4), width=WIDTH)

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
                pygame.draw.polygon(self.surface, (255, 190, 15),
                                   (point_1, point_2, point_3, point_4), width=WIDTH)

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
                pygame.draw.polygon(self.surface, (255, 190, 15),
                                    (point_1, point_2, point_3, point_4), width=WIDTH)

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
                pygame.draw.polygon(self.surface, (255, 190, 15),
                                    (point_1, point_2, point_3, point_4), width=WIDTH)
