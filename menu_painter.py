import pygame
import random
from button import Button


class MenuPainter:
    def __init__(self, screen):
        self.surface = screen
        self.buttons = False

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
        self.buttons = pygame.sprite.Group()
        sprite = Button('play', "st", self.buttons)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 50
        sprite.rect.y = 320
        self.buttons.add(sprite)
        self.buttons.draw(self.surface)
