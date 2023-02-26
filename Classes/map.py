import  opensimplex, random
from pygame import Vector2, Surface, Color, transform, image, display
from typing import Union
from Classes.player import Player
from Classes.tile import Tile, Cave
from Classes.props import *


biomes: dict[Union[float, int], list[str]] = {
    512: ["hell"],
    256: ["lush_cave"],
    128: ["crystal_cave", "haunted_cave"],
    16: ["sand_cave", "cave", "snowy_cave"],
    float("-inf"): ["desert", "forest", "snow"]
}

tile_palettes = {
    "forest": {
        "primary_tile": "dirt",
        "top_tile": "grass"
    },

    "desert": {
        "primary_tile": "sand",
        "top_tile": "sand"
    },

    "snow": {
        "primary_tile": "snowy_dirt",
        "top_tile": "snowy_grass"
    },

    "cave": {
        "primary_tile": "stone",
        "top_tile": "stone"
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
        self.display_surface: Surface = display.get_surface()

        self._tiles: dict[int, dict[int, Tile]] = {}
        self.player: Player = Player((0, 0), self)

        self.scale: float = 0.1
        self.biome_size: float = 0.01

        self.render_distance: int = 32

        opensimplex.random_seed()

    def get_tile(self, position: Vector2) -> Tile:
        if not position.x in self._tiles or not position.y in self._tiles[position.x]:
            self.generate_tile(position)

        return self._tiles[position.x][position.y]

    def set_tile(self, tile: Tile, position: Vector2) -> Tile:
        if not position.x in self._tiles or not position.y in self._tiles[position.x]:
            self.generate_tile(position)
        
        self._tiles[position.x][position.y] = tile
        return tile

    def generate_tile(self, position: Vector2) -> Tile:
        if not position.x in self._tiles:
            self._tiles[position.x] = {}

        for k in biomes.keys():
            if position.y >= k:
                number_range = 2 / len(biomes[k])
                noise_value = opensimplex.noise2(position.x * self.biome_size, 0) + 1
                biome = biomes[k][int(noise_value // number_range)]
                break

        tile_palette = tile_palettes[biome] if biome in tile_palettes else tile_palettes["cave"]
        if position.y < 16:
            noise_value = int(opensimplex.noise2(position.x * self.scale * 0.5, 0) * 10)
            if position.y == noise_value:
                self._tiles[position.x][position.y] = Tile(tile_palette["top_tile"], tile_palette["top_tile"])
            
            elif position.y > noise_value:
                self._tiles[position.x][position.y] = Tile(tile_palette["primary_tile"], tile_palette["primary_tile"])

            else:
                self._tiles[position.x][position.y] = Tile("air", "air", minable=False, can_collide=False)

        else:
            if opensimplex.noise2(position.x * self.scale, position.y * self.scale) < 0:
                self._tiles[position.x][position.y] = Tile(tile_palette["primary_tile"], tile_palette["primary_tile"])
            else:
                self._tiles[position.x][position.y] = Cave(tile_palette["primary_tile"], tile_palette["primary_tile"])
                
        return self._tiles[position.x][position.y]
        
    def render(self) -> None:
        self.display_surface.fill(Color(77, 165, 217))

        offset = Vector2()
        offset.x = self.player.rect.centerx - self.display_surface.get_width() / 2
        offset.y = self.player.rect.centery - self.display_surface.get_height() / 2

        for x in range(int(self.player.position.x) - self.render_distance, int(self.player.position.x) + self.render_distance + 1):
            for y in range(int(self.player.position.y) - self.render_distance, int(self.player.position.y) + self.render_distance + 1):
                offset_rect = Vector2(x, y) * 32 - offset
                self.get_tile(Vector2(x, y)).update(offset_rect)

        offset_rect = self.player.rect.copy()
        offset_rect.center -= offset
        self.display_surface.blit(self.player.image, offset_rect)
        
        if self.player.going_up == True:
            self.player.climb()
        
        if self.player.falling:
            self.display_surface.blit(transform.scale(image.load("Images/PLayer/Parachute.png"), (32, 32)), (offset_rect[0], offset_rect[1] - 32))