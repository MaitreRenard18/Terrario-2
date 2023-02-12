import pygame, random
from Classes.player import Player

class Map:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.tiles = {}
        self.player = Player((0, 0))

        self.sky_color = pygame.Color(77, 165, 217)

        self.offset = pygame.Vector2()
        self.render_distance = 16

        for x in range(-100, 100):
            self.tiles[x] = {}
            for y in range(-100, 100):
                sprite = pygame.sprite.Sprite()
                tile = random.choice(["Stone", "Cave"])
                sprite.image = pygame.transform.scale(pygame.image.load(f"Images/Tiles/{tile}.png"), (32, 32))
                sprite.rect = sprite.image.get_rect()
                sprite.rect.center = pygame.Vector2(x, y) * 32

                self.tiles[x][y] = sprite

    def render(self):
        self.display_surface.fill(self.sky_color)

        self.offset.x = self.player.rect.centerx - self.display_surface.get_width() / 2
        self.offset.y = self.player.rect.centery - self.display_surface.get_height() / 2

        for x in range(int(self.player.position.x) - self.render_distance, int(self.player.position.x) + self.render_distance + 1):
            for y in range(int(self.player.position.y) - self.render_distance, int(self.player.position.y) + self.render_distance + 1):
                sprite = self.tiles[x][y]

                offset_rect = sprite.rect.copy()
                offset_rect.center -= self.offset

                self.display_surface.blit(sprite.image, offset_rect)

        offset_rect = self.player.rect.copy()
        offset_rect.center -= self.offset
        self.display_surface.blit(self.player.image, offset_rect)