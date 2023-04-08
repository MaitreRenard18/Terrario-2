import os
from csv import reader
from random import choice, randint
from typing import Dict, List

from pygame import Vector2

from pathlib import Path

from .map import Map
from .tile import Air, Cave, PropTile, Tile

MODULE_PATH = Path(__file__).parent

props: Dict[str, List[List[str]]] = {}
_props_path = MODULE_PATH / "Props"
for file in os.listdir(_props_path):
    if file.endswith(".csv"):
        file_name = file.replace(".csv", "").lower()
        
        path = os.path.join(_props_path, file)
        with open(path) as csv_file:
            prop = list(reader(csv_file, delimiter=';'))

        props[file_name] = prop


def generate_oak_tree(map: Map, position: Vector2) -> None:
    if not isinstance(map.get_tile(position - (1, 0)), Air) or not isinstance(map.get_tile(position + (1, 0)), Air):
        return

    center = len(props["oak_tree"][-1]) // 2
    for y, row in enumerate(props["oak_tree"]):
        for x, column in enumerate(row):
            if column == "placeholder":
                continue
            
            tile_position = position - (center - x, len(props["oak_tree"]) - y - 1)
            if column in ["oak_leaves", "oak_dark_leaves"]:
                if isinstance(map.get_tile(tile_position), Air):
                    tile = PropTile(column, map.get_tile(tile_position).texture)
                    map.set_tile(tile, tile_position)
                
                continue

            tile = PropTile(column, map.get_tile(tile_position).texture)
            map.set_tile(tile, tile_position)


def generate_plants(map: Map, position: Vector2) -> None:
    if map.get_tile(position).can_collide:
        return
    
    plant = choice(["weed", "tulip"])
    tile = PropTile(plant, map.get_tile(position).texture)
    map.set_tile(tile, position)


def generate_cave_oak_tree(map: Map, position: Vector2) -> None:
    if isinstance(map.get_tile(position - (1, 0)), PropTile) or isinstance(map.get_tile(position + (1, 0)), PropTile):
        return
    
    center = len(props["oak_tree"][-1]) // 2
    for y, row in enumerate(props["oak_tree"]):
        for x, column in enumerate(row):
            if column == "placeholder":
                continue
            
            tile_position = position - (center - x, len(props["oak_tree"]) - y - 1)
            if column in ["oak_leaves", "oak_dark_leaves", "oak_branch"]:
                if isinstance(map.get_tile(tile_position), Cave):
                    tile = PropTile(column, map.get_tile(tile_position).texture)
                    map.set_tile(tile, tile_position)
                
                continue

            tile = PropTile(column, map.get_tile(tile_position).texture)
            map.set_tile(tile, tile_position)


def generate_mushroom(map: Map, position: Vector2) -> None:
    if map.get_tile(position).can_collide:
        return
    
    plant = choice(["red_mushroom", "brown_mushroom"])
    tile = PropTile(plant, map.get_tile(position).texture)
    map.set_tile(tile, position)


def generate_cactus(map: Map, position: Vector2, height: int = None) -> None:
    if height is None:
        height = randint(1, 4)

    if height == 0:
        tile = PropTile("cactus_top", map.get_tile(position).texture)
        map.set_tile(tile, position)
        return
    
    tile = PropTile("cactus", map.get_tile(position).texture)
    map.set_tile(tile, position)
    generate_cactus(map, position - (0, 1), height-1)


def generate_dead_weed(map: Map, position: Vector2) -> None:
    tile = PropTile("dead_weed", map.get_tile(position).texture)
    map.set_tile(tile, position)


def generate_fir(map: Map, position: Vector2) -> None:
    if not isinstance(map.get_tile(position - (1, 0)), Air) or not isinstance(map.get_tile(position + (1, 0)), Air):
        return

    center = len(props["fir"][-1]) // 2
    for y, row in enumerate(props["fir"]):
        for x, column in enumerate(row):
            if column == "placeholder":
                continue
            
            tile_position = position - (center - x, len(props["fir"]) - y - 1)
            if column in ["fir_leaves", "fir_dark_leaves", "fir_snow_covered_leaves"]:
                if isinstance(map.get_tile(tile_position), Air):
                    tile = PropTile(column, map.get_tile(tile_position).texture)
                    map.set_tile(tile, tile_position)
                
                continue

            tile = PropTile(column, map.get_tile(tile_position).texture)
            map.set_tile(tile, tile_position)


def generate_snowy_weed(map: Map, position: Vector2) -> None:
    tile = PropTile("snowy_weed", map.get_tile(position).texture)
    map.set_tile(tile, position)


def generate_snowman(map: Map, position: Vector2) -> None:
    if not isinstance(map.get_tile(position - (1, 0)), Air) or not isinstance(map.get_tile(position + (1, 0)), Air):
        return
    
    map.set_tile(PropTile("snowman_belly", map.get_tile(position).texture), position)
    map.set_tile(PropTile("snowman_torso", map.get_tile(position - (0, 1)).texture), position - (0, 1))
    if isinstance(map.get_tile(position - (1, 1)), Air):
        map.set_tile(PropTile("snowman_right_arm", map.get_tile(position - (1, 1)).texture), position - (1, 1))

    if isinstance(map.get_tile(position + (1, -1)), Air):
        map.set_tile(PropTile("snowman_left_arm", map.get_tile(position + (1, -1)).texture), position + (1, -1))

    map.set_tile(PropTile("snowman_head", map.get_tile(position - (0, 2)).texture), position - (0, 2))


def generate_stalagmite(map: Map, position: Vector2, height: int = None) -> None:
    if height is None:
        if position.y < 20:
            return

        tile = PropTile("stalagmite_base", map.get_tile(position).texture)
        map.set_tile(tile, position)
        return generate_stalagmite(map, position - (0, 1), randint(1, 3))

    if map.get_tile(position).can_collide:
        map.set_tile(Cave(map.get_tile(position).texture), position)

    if height == 0:
        tile = PropTile("stalagmite_tip", map.get_tile(position).texture)
        map.set_tile(tile, position)
        return
    
    if height == 1:
        tile = PropTile("stalagmite_upper_middle", map.get_tile(position).texture)
        map.set_tile(tile, position)
        return generate_stalagmite(map, position - (0, 1), height-1)

    tile = PropTile("stalagmite_middle", map.get_tile(position).texture)
    map.set_tile(tile, position)
    generate_stalagmite(map, position - (0, 1), height-1)
