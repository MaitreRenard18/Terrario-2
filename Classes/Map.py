import pygame, opensimplex, os
from Classes.player import Player

textures = {}
for file in os.listdir("{}\Images\Tiles".format(os.getcwd())):
    if file.endswith(".png"):
        file_name = file.replace(".png", "").lower()
        
        path = "{}\Images\Tiles\{}".format(os.getcwd(), file)
        image = pygame.transform.scale(pygame.image.load(path), (32, 32))
        
        textures[file_name] = image

class Map:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.tiles = {}
        self.player = Player((0, 0))

        self.sky_color = pygame.Color(77, 165, 217)

        self.offset = pygame.Vector2()
        self.render_distance = 32

    def generate_tile(self, x, y):
        if not x in self.tiles:
            self.tiles[x] = {}

        tile = "stone" if opensimplex.noise2(x * 0.1, y * 0.1) < 0 else "cave"
        self.tiles[x][y] = tile

    def render(self):
        self.display_surface.fill(self.sky_color)

        self.offset.x = self.player.rect.centerx - self.display_surface.get_width() / 2
        self.offset.y = self.player.rect.centery - self.display_surface.get_height() / 2

        for x in range(int(self.player.position.x) - self.render_distance, int(self.player.position.x) + self.render_distance + 1):
            for y in range(int(self.player.position.y) - self.render_distance, int(self.player.position.y) + self.render_distance + 1):
                if not x in self.tiles or not y in self.tiles[x]:
                    self.generate_tile(x, y)

                image = textures[self.tiles[x][y]]
                offset_rect = pygame.Vector2(x * 32, y * 32) - self.offset
                self.display_surface.blit(image, offset_rect)

        offset_rect = self.player.rect.copy()
        offset_rect.center -= self.offset
        self.display_surface.blit(self.player.image, offset_rect)