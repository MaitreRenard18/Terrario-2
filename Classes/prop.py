import os
from csv import reader
from typing import TYPE_CHECKING, Dict, List

import pygame
from pygame import Vector2

from .tile import Scaffolding, Tile

if TYPE_CHECKING:
    from .map import Map

csvs: Dict[str, List[List[str]]] = {}
_props_path = os.path.join("Props")
for file in os.listdir(_props_path):
    if file.endswith(".csv"):
        file_name = file.replace(".csv", "").lower()

        path = os.path.join(_props_path, file)
        with open(path) as csv_file:
            csvs[file_name] = list(reader(csv_file, delimiter=';'))


class Prop:
    def __init__(self, map: "Map", position: Vector2, prop_name: str) -> None:
        self.map = map
        self.prop_name: str = prop_name
        self.tiles: Dict[int, Dict[int, Tile]] = _get_prop(prop_name)

        self.position: Vector2 = Vector2(position)
        self.tile_pos: Vector2 = Vector2(position)

        self.speed: float = 0.2
        self.falling: bool = False

    def update(self, position: Vector2) -> None:
        display = pygame.display.get_surface()

        for x, row in self.tiles.items():
            for y, tile in row.items():
                display.blit(tile.texture, position + Vector2(x, -y) * 32)

        self.fall()

    def fall(self) -> None:
        tile_below = self.map.get_tile(self.tile_pos)
        if not tile_below.can_collide or isinstance(tile_below, Scaffolding):
            if not self.falling:
                self.falling = True
                self.speed = 0
                return

            self.speed += 0.1
            self.speed = round(self.speed, 1)
            self.position.y += self.speed
            self.position.y = round(self.position.y, 1)

            if self.position.y >= self.tile_pos.y + 1:
                self.tile_pos.y += 1
                self.position.y = self.tile_pos.y

                index = self.map.props[self.position.x][self.position.y-1].index(self)
                self.map.props[self.position.x][self.position.y-1].pop(index)

                self.map.props[self.position.x] = self.map.props.get(self.position.x, {})
                self.map.props[self.position.x][self.position.y] = self.map.props[self.position.x].get(self.position.y, [])
                self.map.props[self.position.x][self.position.y].append(self)

        else:
            self.falling = False
            self.speed = 0.2

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["tiles"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.tiles = _get_prop(self.prop_name)


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
