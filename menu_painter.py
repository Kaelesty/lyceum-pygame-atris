import pygame
import random
from button import Button


class MenuPainter:
    def __init__(self, screen):
        self.surface = screen
        self.buttons = False

    def init_main_menu(self):
        self.buttons = pygame.sprite.Group()
        sprite = Button('play', "st", self.buttons)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 50
        sprite.rect.y = 320
        self.buttons.add(sprite)
        self.buttons.draw(self.surface)
        self.falls = pygame.sprite.Group()

    def init_selector(self):
        self.buttons = pygame.sprite.Group()

    def upload_buttons(self, buttons):
        self.buttons = buttons

    def draw_waiting(self):
        self.surface.fill((30, 30, 30))
        logo = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                         'logo_0' + '1' + '.png')
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 319
        sprite.rect.y = 4
        logo.add(sprite)
        logo.draw(self.surface)
        button = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                         "push_me.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = random.choice([479, 480, 481, 479, 480, 481, 479, 480, 481, 480,
                                       375, 479, 480, 481, 479, 480, 481, 479, 480, 481,
                                       530, 479, 480, 481, 479, 480, 481, 479, 480, 481,
                                       475, 479, 480, 481, 479, 480, 481, 479, 480, 479])
        sprite.rect.y = random.choice([617, 620, 619, 618])
        button.add(sprite)
        button.draw(self.surface)

    def draw_main_menu(self):
        self.surface.fill((30, 30, 30))
        atris = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite(atris)
        sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                         "background.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 0
        sprite.rect.y = 0
        atris.add(sprite)
        sprite = pygame.sprite.Sprite(atris)
        sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                         "atris.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 5
        sprite.rect.y = 5
        atris.add(sprite)
        atris.draw(self.surface)
        self.buttons.draw(self.surface)
        group = list(self.falls)
        min_y = -666
        while True:
            for i in range(len(group)):
                if min_y > group[i].rect.y or min_y == -666:
                    min_y = group[i].rect.y
                if group[i].rect.y >= 900:
                    del group[i]
                    break
                else:
                    group[i].rect.y += 2
            break
        if min_y > 67 or min_y == -666:
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                             "main_falls.png")
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = random.choice([1200, 1170, 1140, 1110, 1080, 1050, 1020, 990, 960, 930, 900])
            sprite.rect.y = -91
            group.append(sprite)
        self.falls = pygame.sprite.Group()
        for elem in group:
            self.falls.add(elem)
        self.falls.draw(self.surface)

    def draw_selector(self):
        decorations = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                         "border.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 0
        sprite.rect.y = 0
        decorations.add(sprite)
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                         "tetris_border.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 50
        sprite.rect.y = 50
        decorations.add(sprite)
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                         "tetris_st.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 120
        sprite.rect.y = 110
        decorations.add(sprite)
        decorations.draw(self.surface)


