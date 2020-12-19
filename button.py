import pygame

# sizes desc
# standart - 150x32
# extended - 300x100

class Button(pygame.sprite.Sprite):
    def __init__(self, btnname, stat,  *group, size="standart"):
        super().__init__(*group)
        self.name = btnname
        filename = f"{btnname}_{stat}.png"
        image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                  filename)
        self.image = image
        self.rect = self.image.get_rect()
        if size == 'standart':
            self.rect.x = 150
            self.rect.y = 32
        elif size == "extended":
            self.rect.x = 300
            self.rect.y = 100
        self.stat = stat

    def change_stat(self, stat):
        self.stat = stat
        filename = f"{self.name}_{stat}.png"
        image = pygame.image.load("Data\ "[0:-1] + 'Sprites\ '[0:-1] +
                                  filename)
        self.image = image