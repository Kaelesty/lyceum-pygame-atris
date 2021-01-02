import pygame
import random

ONCE_SCALE = 0.8917795292374964


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
                         (self.pos[0] - 3, self.pos[1] - 3, 705, 705), width=1)
        self.draw_center()
        self.draw_top()

    def draw_center(self):
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(self.surface, (255, 190, 15),
                                 (self.pos[0] + 215 + 35 * j, self.pos[1] + 215 + 35 * i, 35, 35), width=1)

    def draw_top(self):
        for i in range(8):
            for j in range(8):
                points =  [(self.pos[0] + int(210 * ONCE_SCALE ** j),
                            self.pos[1] + int(210 * ONCE_SCALE ** i)),
                           (self.pos[0] + int(210 * ONCE_SCALE ** j) + int(140 * ONCE_SCALE ** j),
                            self.pos[1]),
                           (self.pos[0] + int(210 * ONCE_SCALE ** (j + 1)) + int(140 * ONCE_SCALE ** (j + 1)),
                            self.pos[1] + int(210 * ONCE_SCALE ** (i + 1))),
                           (self.pos[0] + int(210 * ONCE_SCALE ** (j + 1)),
                            self.pos[1] + int(210 * ONCE_SCALE ** (i + 1)))
                           ]
                pygame.draw.polygon(self.surface, (255, 190, 15),
                                   points, width=1)
