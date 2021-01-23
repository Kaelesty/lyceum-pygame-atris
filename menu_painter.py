import pygame
import random
from button import Button
from tetris import Tetris
from btris import Btris
from welltris import Welltris
import sqlite3


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

        sprite = Button('notes', "st", self.buttons)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 50
        sprite.rect.y = 360
        self.buttons.add(sprite)

        sprite = Button('exit', "st", self.buttons)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 50
        sprite.rect.y = 400
        self.buttons.add(sprite)

        self.buttons.draw(self.surface)
        self.falls = pygame.sprite.Group()

    def init_selector(self):
        self.buttons = pygame.sprite.Group()
        sprite = Button('classic', "st", self.buttons)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 167
        sprite.rect.y = 220
        self.buttons.add(sprite)

        sprite = Button('normal', "st", self.buttons)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 167
        sprite.rect.y = 320
        self.buttons.add(sprite)

        sprite = Button('hard', "st", self.buttons)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 167
        sprite.rect.y = 420
        self.buttons.add(sprite)
        self.buttons.draw(self.surface)

        sprite = Button('btris_20', "st", self.buttons)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 567
        sprite.rect.y = 220
        self.buttons.add(sprite)

        sprite = Button('btris_10', "st", self.buttons)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 567
        sprite.rect.y = 320
        self.buttons.add(sprite)

        sprite = Button('btris_5', "st", self.buttons)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 567
        sprite.rect.y = 420
        self.buttons.add(sprite)

        sprite = Button('_easy', "st", self.buttons)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 967
        sprite.rect.y = 220
        self.buttons.add(sprite)

        sprite = Button('_normal', "st", self.buttons)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 967
        sprite.rect.y = 320
        self.buttons.add(sprite)

        sprite = Button('_hard', "st", self.buttons)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 967
        sprite.rect.y = 420
        self.buttons.add(sprite)

    def init_classic(self, mode):
        if mode == "classic":
            mode = "easy"
        self.buttons = pygame.sprite.Group()
        self.tetris = Tetris(self.surface, mode, (465, 0))
        self.tetris.new_curr()

    def init_btris(self, size):
        self.btris = Btris(self.surface, size, (10, 10))

    def init_welltris(self, mode):
        self.welltris = Welltris(self.surface, mode, (10, 10))

    def upload_buttons(self, buttons):
        self.buttons = buttons

    def draw_notes(self):
        notes = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                         "notes.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 0
        sprite.rect.y = 0
        notes.add(sprite)
        notes.draw(self.surface)

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
        # Tetris Decorations
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
        sprite.rect.y = 130
        decorations.add(sprite)
        # Btris Decorations
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                         "btris_border.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 450
        sprite.rect.y = 50
        decorations.add(sprite)
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                         "btris_logo.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 520
        sprite.rect.y = 130
        decorations.add(sprite)
        # Welltris Decorations
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                         "welltris_border.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 850
        sprite.rect.y = 50
        decorations.add(sprite)
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                         "welltris_st.png")
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 930
        sprite.rect.y = 130
        decorations.add(sprite)

        decorations.draw(self.surface)
        self.buttons.draw(self.surface)
        self.draw_results()

    def draw_results(self):
        con = sqlite3.connect("Data\ "[0:-1] + "AData.sqlite")
        cur = con.cursor()
        font = pygame.font.Font("Data\ "[0:-1] + "Konstanting.ttf", 30)

        data = cur.execute(f"SELECT Classic_easy FROM Scores").fetchall()[0][0]
        text = font.render("Best:", True, (255, 190, 15))
        text_x = 167
        text_y = 250
        self.surface.blit(text, (text_x, text_y))
        text = font.render(str(data), True, (255, 190, 15))
        text_x = 220
        text_y = 250
        self.surface.blit(text, (text_x, text_y))

        data = cur.execute(f"SELECT Classic_normal FROM Scores").fetchall()[0][0]
        text = font.render("Best:", True, (255, 190, 15))
        text_x = 167
        text_y = 350
        self.surface.blit(text, (text_x, text_y))
        text = font.render(str(data), True, (255, 190, 15))
        text_x = 220
        text_y = 350
        self.surface.blit(text, (text_x, text_y))

        data = cur.execute(f"SELECT Classic_hard FROM Scores").fetchall()[0][0]
        text = font.render("Best:", True, (255, 190, 15))
        text_x = 167
        text_y = 450
        self.surface.blit(text, (text_x, text_y))
        text = font.render(str(data), True, (255, 190, 15))
        text_x = 220
        text_y = 450
        self.surface.blit(text, (text_x, text_y))

        data = cur.execute(f"SELECT Btris_20 FROM Scores").fetchall()[0][0]
        text = font.render("Best:", True, (255, 190, 15))
        text_x = 567
        text_y = 250
        self.surface.blit(text, (text_x, text_y))
        text = font.render(str(data), True, (255, 190, 15))
        text_x = 620
        text_y = 250
        self.surface.blit(text, (text_x, text_y))

        data = cur.execute(f"SELECT Btris_10 FROM Scores").fetchall()[0][0]
        text = font.render("Best:", True, (255, 190, 15))
        text_x = 567
        text_y = 350
        self.surface.blit(text, (text_x, text_y))
        text = font.render(str(data), True, (255, 190, 15))
        text_x = 620
        text_y = 350
        self.surface.blit(text, (text_x, text_y))

        data = cur.execute(f"SELECT Btris_5 FROM Scores").fetchall()[0][0]
        text = font.render("Best:", True, (255, 190, 15))
        text_x = 567
        text_y = 450
        self.surface.blit(text, (text_x, text_y))
        text = font.render(str(data), True, (255, 190, 15))
        text_x = 620
        text_y = 450
        self.surface.blit(text, (text_x, text_y))

        data = cur.execute(f"SELECT _easy FROM Scores").fetchall()[0][0]
        text = font.render("Best:", True, (255, 190, 15))
        text_x = 967
        text_y = 250
        self.surface.blit(text, (text_x, text_y))
        text = font.render(str(data), True, (255, 190, 15))
        text_x = 1020
        text_y = 250
        self.surface.blit(text, (text_x, text_y))

        data = cur.execute(f"SELECT _normal FROM Scores").fetchall()[0][0]
        text = font.render("Best:", True, (255, 190, 15))
        text_x = 967
        text_y = 350
        self.surface.blit(text, (text_x, text_y))
        text = font.render(str(data), True, (255, 190, 15))
        text_x = 1020
        text_y = 350
        self.surface.blit(text, (text_x, text_y))

        data = cur.execute(f"SELECT _hard FROM Scores").fetchall()[0][0]
        text = font.render("Best:", True, (255, 190, 15))
        text_x = 967
        text_y = 450
        self.surface.blit(text, (text_x, text_y))
        text = font.render(str(data), True, (255, 190, 15))
        text_x = 1020
        text_y = 450
        self.surface.blit(text, (text_x, text_y))


    def draw_and_step(self):
        self.tetris.make_step()
        self.tetris.draw_self()

    def draw_and_step_w(self):
        self.welltris.make_step()
        self.welltris.draw_self()
