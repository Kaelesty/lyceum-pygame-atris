import pygame

# sizes desc
# standard - 150x32
# extended - 300x100


class Button(pygame.sprite.Sprite):
    def __init__(self, button_name, stat,  *group, size="standard"):
        super().__init__(*group)
        self.name = button_name
        filename = f"{button_name}_{stat}.png"
        image = pygame.image.load("Data\\" + "Sprites\\" +
                                  filename)
        self.image = image
        self.rect = self.image.get_rect()
        if size == 'standard':
            self.rect.x = 150
            self.rect.y = 32
        elif size == "extended":
            self.rect.x = 300
            self.rect.y = 100
        self.stat = stat

    def change_stat(self, stat):
        self.stat = stat
        filename = f"{self.name}_{stat}.png"
        image = pygame.image.load("Data\\" + "Sprites\\" +
                                  filename)
        self.image = image
