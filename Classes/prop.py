from typing import Dict, List
from csv import reader
import os

import pygame
from pygame import Vector2

from Classes.tile import Tile
from Classes.map import Map


csvs: Dict[str, List[List[str]]] = {}
_props_path = os.path.join("Props")
for file in os.listdir(_props_path):
    if file.endswith(".csv"):
        file_name = file.replace(".csv", "").lower()

        path = os.path.join(_props_path, file)
        with open(path) as csv_file:
            csvs[file_name] = list(reader(csv_file, delimiter=';'))


class Prop:
    def __init__(self, map: Map, position: Vector2, prop_name: str) -> None:
        self.map = map
        self.position: Vector2 = position
        self.prop_name: str = prop_name
        self.tiles: Dict[int, Dict[int, Tile]] = _get_prop_from_file(prop_name)

    def update(self, position: Vector2):
        for x, row in self.tiles.items():
            for y, tile in row.items():
                display = pygame.display.get_surface()
                display.blit(tile.texture, position + Vector2(x, -y) * 32)

        if not self.map.get_tile(self.position).can_collide:
            self.map.props[self.position.x].pop(self.position.y)
            self.position = self.position + Vector2(0, 1)
            self.map.props[self.position.x][self.position.y] = self


def _get_prop_from_file(prop_name: str) -> Dict[int, Dict[int, Tile]]:
    prop = {}
    center = len(csvs[prop_name][-1]) // 2
    for y, row in enumerate(csvs[prop_name]):
        for x, value in enumerate(row):
            if value == "placeholder":
                continue

            if x - center not in prop:
                prop[x - center] = {}

            prop[x - center][len(csvs[prop_name]) - y] = Tile(value, float("inf"), False)

    return prop