import pygame
from Classes.player import Player

class Map:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.tiles = {}

        self.sprite_group = CameraGroup()

        self.Setup()

    def Setup(self):
        self.generate()
        self.player = Player((0, 0), self.sprite_group)

    def update(self):
        self.display_surface.fill("black")
        self.sprite_group.custom_draw(self.player)
        self.sprite_group.update()

    def generate(self):
        for x in range(50):
            self.tiles[x] = {}
            for y in range(50):
                tile = pygame.sprite.Sprite(self.sprite_group)
                tile.image = pygame.transform.scale(pygame.image.load("Images/Tiles/Stone.png"), (32, 32))
                tile.rect = tile.image.get_rect()
                tile.rect.center = pygame.Vector2(x, y) * 32

                self.tiles[x][y] = tile

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.display_surface.get_width() / 2
        self.offset.y = player.rect.centery - self.display_surface.get_height() / 2

        for sprite in self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset

            self.display_surface.blit(sprite.image, offset_rect)