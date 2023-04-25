import os
from csv import reader
from typing import TYPE_CHECKING, Dict, List, Union

from pygame import Vector2

from Classes.tile import Scaffolding, Tile, AnimatedTile

if TYPE_CHECKING:
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
    def __init__(self, map: "Map", position: Vector2, prop_name: str) -> None:
        self.map = map
        self.prop_name: str = prop_name
        self.tiles: Dict[int, Dict[int, Tile]] = _get_prop(prop_name)

        self.position: Vector2 = Vector2(position)
        self.relative_position: Vector2 = Vector2(position)

        self.speed: float = 0

    def update(self, position: Vector2) -> None:
        for x, row in self.tiles.items():
            for y, tile in row.items():
                tile.update(position + Vector2(x, -y) * 32)

        tile_below = self.map.get_tile(self.relative_position)
        if not tile_below.can_collide or isinstance(tile_below, Scaffolding):
            self.fall()
        else:
            self.speed = 0

    def change_position(self, position: Union[Vector2, tuple]):
        x, y = (int(position.x), int(position.y)) if isinstance(position, Vector2) else (position[0], position[1])

        self.map.remove_prop(self, self.relative_position)

        self.position = Vector2(x, y)
        self.relative_position = Vector2(x, y)

        self.map.add_prop(self, position)

    def fall(self) -> None:
        """
        Fait tomber le prop.
        La vitesse du prop augmente au fur et à mesure qu'il tombe.
        La limite de vitesse du prop est d'une tile.
        """

        self.speed += round(0.1, 1)
        self.position.y += self.speed
        self.position.y = round(self.position.y, 1)

        if self.position.y >= self.relative_position.y + 1:
            self.change_position(self.relative_position + (0, 1))

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["tiles"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.tiles = _get_prop(self.prop_name)


props: Dict[str, Dict[int, Dict[int, Tile]]] = {}


def _get_prop(prop_name: str) -> Dict[int, Dict[int, Tile]]:
    if prop_name in props:
        return props[prop_name]

    prop = {}
    if not csvs.get(prop_name, False):
        if prop_name == "fire":
            return {0: {1: AnimatedTile("Fire", 12)}}
        else:
            return {0: {1: Tile(prop_name, float("inf"), False)}}

    center = len(csvs[prop_name][-1]) // 2
    for y, row in enumerate(csvs[prop_name]):
        for x, value in enumerate(row):
            if value == "placeholder":
                continue

            if x - center not in prop:
                prop[x - center] = {}

            prop[x - center][len(csvs[prop_name]) - y] = Tile(value, float("inf"), False)

    props[prop_name] = prop
    return props[prop_name]
