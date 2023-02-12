import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)

        self.image = pygame.image.load("Images/PLayer/Drill.png")
        self.rect = self.image.get_rect()