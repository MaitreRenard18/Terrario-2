from random import randint, choice

from pygame import Vector2

from Classes.tile import Tile

def _place_tile(map, type: str, x: int, y: int) -> Tile:
    x, y = int(x), int(y)
    
    if map.get_tile(Vector2(x, y)).type == "air":
        return map.set_tile(Tile(type, type, minable=False, can_collide=False), Vector2(x, y))

def generate_nothing(map, x: int, y:int) -> None:
    return None

def generate_cactus(map, x: int, y: int, height: int = None) -> None:
    x, y = int(x), int(y)

    if height is None:
        height = randint(1, 4)

    if height == 0:
        _place_tile(map, "cactus_top", x, y)
        return
    
    _place_tile(map, "cactus", x, y)
    generate_cactus(map, x, y-1, height-1)


def generate_dead_weed(map, x: int, y:int) -> None:
    _place_tile(map, "dead_weed", x, y)


def generate_tree(map, x: int, y: int) -> None:
    x, y = int(x), int(y)

    if map.get_tile(Vector2(x+1, y)).type == "oak_trunk" or map.get_tile(Vector2(x-1, y)).type == "oak_trunk":
        return

    map.set_tile(Tile("oak_trunk", "oak_trunk", minable=False, can_collide=False), Vector2(x, y))
    map.set_tile(Tile("oak_trunk", "oak_trunk", minable=False, can_collide=False), Vector2(x, y-1))
    map.set_tile(Tile("oak_branch", "oak_branch", minable=False, can_collide=False), Vector2(x+1, y-1))
    map.set_tile(Tile("oak_leaves_covered_trunk", "oak_leaves_covered_trunk", minable=False, can_collide=False), Vector2(x, y-2))
    _place_tile(map, "oak_dark_leaves", x, y-3)

    for i in range(y-3, y-1):
        _place_tile(map, "oak_dark_leaves", x-1, i)
    for i in range(y-3, y-1):
        _place_tile(map, "oak_dark_leaves", x+1, i)

    for i in range(y-3, y-1):
        _place_tile(map, "oak_leaves", x-2, i)
    for i in range(y-3, y-1):
        _place_tile(map, "oak_leaves", x+2, i)

    for i in range(x-1, x+2):
        _place_tile(map, "oak_leaves", i, y-4)


def generate_plants(map, x: int, y:int) -> None:
    plant = choice(["weed", "tulip"])
    _place_tile(map, plant, x, y)


def generate_snowy_tree(map, x: int, y: int):
    x, y = int(x), int(y)

    if map.get_tile(Vector2(x+1, y)).type != "air" or map.get_tile(Vector2(x-1, y)).type != "air":
        return
    
    map.set_tile(Tile("fir_trunk", "fir_trunk", minable=False, can_collide=False), Vector2(x, y))
    map.set_tile(Tile("fir_leaves_covered_trunk", "fir_leaves_covered_trunk", minable=False, can_collide=False), Vector2(x, y-1))
    _place_tile(map, "fir_leaves", x+1, y-1)
    _place_tile(map, "fir_leaves", x-1, y-1)
    for i in range(-6, -1):
        map.set_tile(Tile("fir_dark_leaves_covered_trunk", "fir_dark_leaves_covered_trunk", minable=False, can_collide=False), Vector2(x, y+i))
    for i in range(-4, -1):
        _place_tile(map, "fir_dark_leaves", x-1, y+i)
    for i in range(-4, -1):
        _place_tile(map, "fir_dark_leaves", x+1, y+i)

    _place_tile(map, "fir_leaves", x-2, y-2)
    _place_tile(map, "fir_leaves", x-2, y-3)
    _place_tile(map, "fir_snow_covered_leaves", x-2, y-4)

    _place_tile(map, "fir_leaves", x+2, y-2)
    _place_tile(map, "fir_leaves", x+2, y-3)
    _place_tile(map, "fir_snow_covered_leaves", x+2, y-4)

    _place_tile(map, "fir_leaves", x-1, y-5)
    _place_tile(map, "fir_snow_covered_leaves", x-1, y-6)

    _place_tile(map, "fir_leaves", x+1, y-5)
    _place_tile(map, "fir_snow_covered_leaves", x+1, y-6)

    _place_tile(map, "fir_leaves", x, y-7)
    _place_tile(map, "fir_snow_covered_leaves", x, y-8)

def generate_snowman(map, x: int, y: int) -> None:
    x, y = int(x), int(y)

    if map.get_tile(Vector2(x+1, y)).type == "snowman_belly" or map.get_tile(Vector2(x-1, y)).type == "snowman_belly":
        return
    
    map.set_tile(Tile("snowman_belly", "snowman_belly", minable=False, can_collide=False), Vector2(x, y))
    map.set_tile(Tile("snowman_torso", "snowman_torso", minable=False, can_collide=False), Vector2(x, y-1))
    _place_tile(map, "snowman_right_arm", x-1, y-1)
    _place_tile(map, "snowman_left_arm", x+1, y-1)
    map.set_tile(Tile("snowman_head", "snowman_head", minable=False, can_collide=False), Vector2(x, y-2))

def generate_snowy_weed(map, x: int, y: int) -> None:
    _place_tile(map, "snowy_weed", x, y)