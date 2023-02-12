import pygame
from Classes.player import Player

class Map:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        
        self.sprite_group = pygame.sprite.Group()

        self.Setup()

    def Setup(self):    
        self.player = Player((0, 0), self.sprite_group)

    def run(self):
        self.display_surface.fill("black")
        self.sprite_group.draw(self.display_surface)
        self.sprite_group.update()