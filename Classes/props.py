from random import randint
from Classes.tile import Tile

def _place_tile(map, type: str, x: int, y: int) -> Tile:
    if not map.get_tile(x, y).can_collide:
        return map.set_tile(Tile(type, type, minable=False, can_collide=False), x, y)


def generate_cactus(map, x: int, y: int, height: int = None) -> None:
    if height is None:
        height = randint(1, 4)

    if height == 0:
        _place_tile(map, "cactus_top", x, y)
        return
    
    _place_tile(map, "cactus", x, y)
    generate_cactus(map, x, y-1, height-1)


def generate_snowman(map, x: int, y: int) -> None:
    _place_tile(map, "snowman_belly", x, y)
    _place_tile(map, "snowman_torso", x, y-1)
    _place_tile(map, "snowman_right_arm", x-1, y-1)
    _place_tile(map, "snowman_left_arm", x+1, y-1)
    _place_tile(map, "snowman_head", x, y-2)


def generate_tree(map, x: int, y: int) -> None:
    map.set_tile(Tile("oak_trunk", "oak_trunk", minable=False, can_collide=False), x, y)
    map.set_tile(Tile("oak_trunk", "oak_trunk", minable=False, can_collide=False), x, y-1)
    map.set_tile(Tile("oak_branch", "oak_branch", minable=False, can_collide=False), x+1, y-1)
    map.set_tile(Tile("oak_leaves_covered_trunk", "oak_leaves_covered_trunk", minable=False, can_collide=False), x, y-2)
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


def generate_snowy_tree(map, x, y, height):
    pass