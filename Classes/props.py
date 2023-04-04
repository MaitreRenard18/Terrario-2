import os
from csv import reader
from random import choice, randint
from typing import Dict, List

from pygame import Vector2

from Classes.map import Map
from Classes.tile import Air, Cave, PropTile, Tile

props: Dict[str, List[List[str]]] = {}
_props_path = os.path.join("Props")
for file in os.listdir(_props_path):
    if file.endswith(".csv"):
        file_name = file.replace(".csv", "").lower()
        
        path = os.path.join(_props_path, file)
        with open(path) as file:
            prop = list(reader(file, delimiter=';'))

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
                    tile = PropTile(column)
                    map.set_tile(tile, tile_position)
                
                continue

            tile = PropTile(column)
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
        height =  randint(1, 4)

    if height == 0:
        tile = Tile("cactus_top", can_collide=False, hardness=float("inf"))
        map.set_tile(tile, position)
        return
    
    tile = Tile("cactus", can_collide=False, hardness=float("inf"))
    map.set_tile(tile, position)
    generate_cactus(map, position - (0, 1), height-1)


def generate_dead_weed(map: Map, position: Vector2) -> None:
    tile = Tile("dead_weed", can_collide=False, hardness=float("inf"))
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
                    tile = Tile(column, can_collide=False, hardness=float("inf"))
                    map.set_tile(tile, tile_position)
                
                continue

            tile = Tile(column, can_collide=False, hardness=float("inf"))
            map.set_tile(tile, tile_position)


def generate_snowy_weed(map: Map, position: Vector2) -> None:
    tile = Tile("snowy_weed", can_collide=False, hardness=float("inf"))
    map.set_tile(tile, position)


def generate_snowman(map: Map, position: Vector2) -> None:
    if not isinstance(map.get_tile(position - (1, 0)), Air) or not isinstance(map.get_tile(position + (1, 0)), Air):
        return
    
    map.set_tile(Tile("snowman_belly", hardness=float("inf"), can_collide=False), position)
    map.set_tile(Tile("snowman_torso", hardness=float("inf"), can_collide=False), position - (0, 1))
    if isinstance(map.get_tile(position - (1, 1)), Air):
        map.set_tile(Tile("snowman_right_arm", hardness=float("inf"), can_collide=False), position - (1, 1))

    if isinstance(map.get_tile(position + (1, -1)), Air):
        map.set_tile(Tile("snowman_left_arm", hardness=float("inf"), can_collide=False), position + (1, -1))

    map.set_tile(Tile("snowman_head", hardness=float("inf"), can_collide=False), position - (0, 2))


def generate_stalagmite(map: Map, position: Vector2, height: int = None) -> None:
    if height is None:
        if position.y < 20:
            return

        tile = PropTile("stalagmite_base", map.get_tile(position).texture)
        map.set_tile(tile, position)
        return generate_stalagmite(map, position - (0, 1), randint(1, 3))

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
