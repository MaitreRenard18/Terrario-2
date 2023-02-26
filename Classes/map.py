import pygame, opensimplex, random
from pygame import Vector2
from Classes.player import Player
from Classes.tile import Tile, Cave
from Classes.props import *

biomes = {
    float("-inf"): ["forest", "desert", "snow"],
    16: ["cave", "sand_cave", "snowy_cave"],
    128: ["crystal_cave", "haunted_cave"],
    256: ["lush_cave"],
    512: ["hell"]
}

tile_palette = {
    "forest": {
        "background": "air",
        "primary_tile": "dirt",
        "top_tile": "grass"
    },

    "desert": {
        "background": "air",
        "primary_tile": "sand",
        "top_tile": "sand"
    },

    "snow": {
        "background": "air",
        "primary_tile": "dirt",
        "top_tile": "snowy_grass"
    }
}

props = {
    "forest": [generate_tree],
    "desert": [generate_cactus],
    "snow": [generate_snowy_tree]
}

ores = {
    "forest": [],
    "desert": [],
    "snow": []
}

class Map:
    def __init__(self) -> None:
        self.display_surface: pygame.Surface = pygame.display.get_surface()

        self._tiles: dict = {}
        self.player: Player = Player((0, 0), self)

        self.scale: float = 0.1

        self.render_distance: int = 32

        opensimplex.random_seed()

    def get_tile(self, position: Vector2) -> Tile:
        if not position.x in self.tiles or not position.y in self.tiles[position.x]:
            self.generate_tile(position)

        return self._tiles[position.x][position.y]

    def set_tile(self, tile: Tile, position: Vector2) -> Tile:
        if not position.x in self.tiles or not position.y in self.tiles[position.x]:
            self.generate_tile(position)
        
        self._tiles[position.x][position.y] = tile
        return Tile

    def render(self) -> None:
        self.display_surface.fill(pygame.Color(77, 165, 217))

        offset = Vector2()
        offset.x = self.player.rect.centerx - self.display_surface.get_width() / 2
        offset.y = self.player.rect.centery - self.display_surface.get_height() / 2

        for x in range(int(self.player.position.x) - self.render_distance, int(self.player.position.x) + self.render_distance + 1):
            for y in range(int(self.player.position.y) - self.render_distance, int(self.player.position.y) + self.render_distance + 1):
                if not x in self.tiles or not y in self.tiles[x]:
                    self.generate_tile(x, y)

                offset_rect = pygame.Vector2(x, y) * 32 - offset
                self.tiles[x][y].update(offset_rect)

        offset_rect = self.player.rect.copy()
        offset_rect.center -= offset
        self.display_surface.blit(self.player.image, offset_rect)
        
        if self.player.going_up == True:
            self.player.climb()
        
        if self.player.falling:
            self.display_surface.blit(pygame.transform.scale(pygame.image.load("Images/PLayer/Parachute.png"), (32, 32)), (offset_rect[0], offset_rect[1] - 32))
