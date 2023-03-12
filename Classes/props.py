from random import randint, choice
from typing import List, Dict
from csv import reader
import os

from pygame import Vector2

from Classes.tile import Tile
from Classes.map import Map

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
    if map.get_tile(position - (1, 0)).type != "air" or map.get_tile(position + (1, 0)).type != "air":
        return

    center = len(props["oak_tree"][-1]) // 2
    for y, row in enumerate(props["oak_tree"]):
        for x, column in enumerate(row):
            if column == "placeholder":
                continue
            
            tile_position = position - (center - x, len(props["oak_tree"]) - y - 1)
            if column in ["oak_leaves", "oak_dark_leaves"]:
                if map.get_tile(tile_position).type == "air":
                    tile = Tile(column, column, can_collide=False, minable=False)
                    map.set_tile(tile, tile_position)
                
                continue

            tile = Tile(column, column, can_collide=False, minable=False)
            map.set_tile(tile, tile_position)

def generate_plants(map: Map, position: Vector2) -> None:
    plant = choice(["weed", "tulip"])
    tile = Tile(plant, plant, can_collide=False, minable=False)
    map.set_tile(tile, position)

def generate_cactus(map: Map, position: Vector2, height: int = None) -> None:
    if height is None:
        height =  randint(1, 4)

    if height == 0:
        tile = Tile("cactus_top", "cactus_top", can_collide=False, minable=False)
        map.set_tile(tile, position)
        return
    
    tile = Tile("cactus", "cactus", can_collide=False, minable=False)
    map.set_tile(tile, position)
    generate_cactus(map, position - (0, 1), height-1)

def generate_dead_weed(map: Map, position: Vector2) -> None:
    tile = Tile("dead_weed", "dead_weed", can_collide=False, minable=False)
    map.set_tile(tile, position)

def generate_fir(map: Map, position: Vector2) -> None:
    if map.get_tile(position - (1, 0)).type != "air" or map.get_tile(position + (1, 0)).type != "air":
        return

    center = len(props["fir"][-1]) // 2
    for y, row in enumerate(props["fir"]):
        for x, column in enumerate(row):
            if column == "placeholder":
                continue
            
            tile_position = position - (center - x, len(props["fir"]) - y - 1)
            if column in ["fir_leaves", "fir_dark_leaves", "fir_snow_covered_leaves"]:
                if map.get_tile(tile_position).type == "air":
                    tile = Tile(column, column, can_collide=False, minable=False)
                    map.set_tile(tile, tile_position)
                
                continue

            tile = Tile(column, column, can_collide=False, minable=False)
            map.set_tile(tile, tile_position)

def generate_snowy_weed(map: Map, position: Vector2) -> None:
    tile = Tile("snowy_weed", "snowy_weed", can_collide=False, minable=False)
    map.set_tile(tile, position)

def generate_snowman(map: Map, position: Vector2) -> None:
    if map.get_tile(position - (1, 0)).type == "snowman_belly" or map.get_tile(position + (1, 0)).type == "snowman_belly":
        return
    
    map.set_tile(Tile("snowman_belly", "snowman_belly", minable=False, can_collide=False), position)
    map.set_tile(Tile("snowman_torso", "snowman_torso", minable=False, can_collide=False), position - (0, 1))
    if map.get_tile(position - (1, 1)).type == "air":
        map.set_tile(Tile("snowman_right_arm", "snowman_right_arm", minable=False, can_collide=False), position - (1, 1))

    if map.get_tile(position + (1, -1)).type == "air":
        map.set_tile(Tile("snowman_left_arm", "snowman_left_arm", minable=False, can_collide=False), position + (1, -1))

    map.set_tile(Tile("snowman_head", "snowman_head", minable=False, can_collide=False), position - (0, 2))

def generate_stalagmite(map: Map, position: Vector2, height: int = None) -> None:
    if height is None:
        if position.y < 20:
            return

        tile = Tile("stalagmite_base", "stalagmite_base", can_collide=False, minable=False)
        map.set_tile(tile, position)
        return generate_stalagmite(map, position - (0, 1), randint(1, 3))

    if height == 0:
        tile = Tile("stalagmite_tip", "stalagmite_tip", can_collide=False, minable=False)
        map.set_tile(tile, position)
        return
    
    if height == 1:
        tile = Tile("stalagmite_upper_middle", "stalagmite_upper_middle", can_collide=False, minable=False)
        map.set_tile(tile, position)
        return generate_stalagmite(map, position - (0, 1), height-1)

    tile = Tile("stalagmite_middle", "stalagmite_middle", can_collide=False, minable=False)
    map.set_tile(tile, position)
    generate_stalagmite(map, position - (0, 1), height-1)