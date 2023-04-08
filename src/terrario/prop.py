import os
from csv import reader
from typing import TYPE_CHECKING, Dict, List

import pygame
from pygame import Vector2

from pathlib import Path

from .tile import Scaffolding, Tile

if TYPE_CHECKING:
    from .map import Map

MODULE_PATH = Path(__file__).parent

csvs: Dict[str, List[List[str]]] = {}
_props_path = MODULE_PATH / "Props"
for file in os.listdir(_props_path):
    if file.endswith(".csv"):
        file_name = file.replace(".csv", "").lower()

        path = os.path.join(_props_path, file)
        with open(path) as csv_file:
            csvs[file_name] = list(reader(csv_file, delimiter=';'))


class Prop:
    large_hit_box: bool = False

    def __init__(self, map: "Map", position: Vector2, prop_name: str) -> None:
        self.map = map
        self.position: Vector2 = position
        self.prop_name: str = prop_name
        self.tiles: Dict[int, Dict[int, Tile]] = _get_prop(prop_name)

    def update(self, position: Vector2) -> None:
        display = pygame.display.get_surface()
        can_fall = True

        for x, row in self.tiles.items():
            for y, tile in row.items():
                display.blit(tile.texture, position + Vector2(x, -y) * 32)

                tile_underneath = self.map.get_tile(self.position + Vector2(x, -y + 1))
                if self.large_hit_box and tile_underneath.can_collide and not isinstance(tile_underneath, Scaffolding):
                    can_fall = False

        if not self.large_hit_box:
            tile_underneath = self.map.get_tile(self.position)
            if tile_underneath.can_collide and not isinstance(tile_underneath, Scaffolding):
                can_fall = False

        if can_fall:
            self.map.props[self.position.x].pop(self.position.y)
            self.position = self.position + Vector2(0, 1)
            self.map.props[self.position.x][self.position.y] = self


def _get_prop(prop_name: str) -> Dict[int, Dict[int, Tile]]:
    prop = {}
    if not csvs.get(prop_name, False):
        prop = {0: {1: Tile(prop_name, float("inf"), False)}}
        return prop

    center = len(csvs[prop_name][-1]) // 2
    for y, row in enumerate(csvs[prop_name]):
        for x, value in enumerate(row):
            if value == "placeholder":
                continue

            if x - center not in prop:
                prop[x - center] = {}

            prop[x - center][len(csvs[prop_name]) - y] = Tile(value, float("inf"), False)

    return prop
