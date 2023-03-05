from typing import Union, Dict, List, Callable

import pygame,  opensimplex
from pygame import Vector2, Surface, Color, transform, image, display

from Classes.player import Player
from Classes.tile import Tile, Cave, Air

class Map:
    def __init__(self) -> None:
        self.display_surface: Surface = display.get_surface()

        self._tiles: Dict[int, Dict[int, Tile]] = {}
        self.player: Player = Player((0, -1), self)

        self.scale: float = 0.1
        self.biome_size: float = 0.0075

        self.render_distance: int = 32

        opensimplex.seed = randint(0, 2048)

    def get_tile(self, position: Vector2) -> Tile:
        position.x, position.y = int(position.x), int(position.y)
        if not int(position.x) in self._tiles or not int(position.y) in self._tiles[position.x]:
            self.generate_tile(position.copy())

        return self._tiles[position.x][position.y]

    def set_tile(self, tile: Tile, position: Vector2) -> Tile:
        position.x, position.y = int(position.x), int(position.y)
        if not position.x in self._tiles or not position.y in self._tiles[position.x]:
            self.generate_tile(position.copy())
        
        self._tiles[position.x][position.y] = tile
        return tile

    def generate_tile(self, position: Vector2) -> Tile:
        if not position.x in self._tiles:
            self._tiles[position.x] = {}
        for k in biomes.keys():
            if position.y + randint(0, 3) >= k:
                number_range = 2 / len(biomes[k])
                noise_value = opensimplex.noise2((position.x + randint(0, 3)) * self.biome_size, 0) + 1
                biome = biomes[k][int(noise_value // number_range)]
                break
        
        tile_palette = tile_palettes[biome] if biome in tile_palettes else tile_palettes["cave"]
        if position.y - randint(0, 3) < 16:
            noise_value = int(opensimplex.noise2(position.x * self.scale * 0.25, 0) * 8)
            if position.y == noise_value:
                if "floor_tile" in tile_palette:
                    self._tiles[position.x][position.y] = Tile(tile_palette["floor_tile"], tile_palette["floor_tile"])

                else:
                    self._tiles[position.x][position.y] = Tile(tile_palette["primary_tile"], tile_palette["primary_tile"])
            
            elif position.y > noise_value:
                self._tiles[position.x][position.y] = Tile(tile_palette["primary_tile"], tile_palette["primary_tile"])

            else:
                self._tiles[position.x][position.y] = Air()

        else:
            if opensimplex.noise2(position.x * self.scale, position.y * self.scale) < 0:
                self._tiles[position.x][position.y] = Tile(tile_palette["primary_tile"], tile_palette["primary_tile"])
                
                if "floor_tile" in tile_palette and not self.get_tile(position - Vector2(0, 1)).can_collide:
                    self._tiles[position.x][position.y] = Tile(tile_palette["floor_tile"], tile_palette["floor_tile"])
                
                if "ceiling_tile" in tile_palette and not self.get_tile(position + Vector2(0, 1)).can_collide:
                    self._tiles[position.x][position.y] = Tile(tile_palette["ceiling_tile"], tile_palette["ceiling_tile"])

            else:
                self._tiles[position.x][position.y] = Cave(tile_palette["primary_tile"], tile_palette["primary_tile"])
        
        #Génération des props
        if self._tiles[position.x][position.y].can_collide and not self.get_tile(position - Vector2(0, 1)).can_collide and biome in props:
            if randint(1, 4) == 1:
                choice(props[biome])(self, position - (0, 1))

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
        
        self.player.facing(self.player.going)

        self.display_surface.blit(self.player.image, offset_rect)
        self.display_surface.blit(self.player.tip, (offset_rect.x + self.player.going[1][0] * 32, offset_rect.y + self.player.going[1][1] * 32))
        
        if self.player.going[0] == "up":
            self.player.climb()

from Classes.props import *
biomes: Dict[Union[float, int], List[str]] = {
    #512: ["hell"],
    #256: ["crystal_cave", "haunted_cave"],
    #128: ["lush_cave"],
    16: ["sand_cave", "cave", "ice_cave"],
    float("-inf"): ["desert", "forest", "snowy_forest"]
}

tile_palettes: Dict[str, Dict[str, str]] = {
    "forest": {
        "primary_tile": "dirt",
        "floor_tile": "grass"
    },

    "desert": {
        "primary_tile": "sand"
    },

    "snowy_forest": {
        "primary_tile": "snowy_dirt",
        "floor_tile": "snowy_grass"
    },

    "cave": {
        "primary_tile": "stone",
    },

    "sand_cave": {
        "primary_tile": "sandstone",
    },

    "ice_cave": {
        "primary_tile": "ice",
    },

    "lush_cave": {
        "primary_tile": "tuff",
        "floor_tile": "mossy_tuff",
        "ceiling_tile": "tuff"
    },
}

props: Dict[str, List[Callable[[map, Vector2], None]]] = {
    "forest": [generate_oak_tree, generate_plants, generate_plants], 
    "desert": [generate_cactus, generate_dead_weed, generate_dead_weed],
    "snowy_forest": [generate_fir, generate_fir, generate_snowy_weed, generate_snowy_weed, generate_snowman],

    "cave": [generate_stalagmite]
}

ores: Dict[str, list[str]] = {
    "forest": [],
    "desert": [],
    "snowy_forest": []
}