from Classes.tile import Tile


def generate_cactus(map, x: int, y: int, height: int) -> None:
    if height == 0:
        map.tiles[x][y] = Tile("cactus_top", "cactus_top", minable=False, can_collide=False)
        return
    
    map.tiles[x][y] = Tile("cactus", "cactus", minable=False, can_collide=False)
    generate_cactus(map, x, y-1, height-1)


def generate_snowman(map, x: int, y: int) -> None:
    map.set_tile(x, y, Tile("snowman_belly", "snowman_belly", minable=False, can_collide=False))
    map.set_tile(x, y-1, Tile("snowman_torso", "snowman_torso", minable=False, can_collide=False))
    if map.get_tile(x-1, y-1).type == "air":
        map.set_tile(x-1, y-1, Tile("snowman_right_arm", "snowman_right_arm", minable=False, can_collide=False))
    if map.get_tile(x+1, y-1).type == "air":
        map.set_tile(x+1, y-1, Tile("snowman_left_arm", "snowman_left_arm", minable=False, can_collide=False))
    map.set_tile(x, y-2, Tile("snowman_head", "snowman_head", minable=False, can_collide=False))


def generate_tree(map, x: int, y: int) -> None:
    def _place_tile(leave_type, x, y):
        if map.get_tile(x, y).type == "air":
            map.set_tile(x, y, Tile(leave_type, leave_type, minable=False, can_collide=False))
    
    map.set_tile(x, y, Tile("oak_trunk", "oak_trunk", minable=False, can_collide=False))
    map.set_tile(x, y-1, Tile("oak_trunk", "oak_trunk", minable=False, can_collide=False))
    map.set_tile(x+1, y-1, Tile("oak_branch", "oak_branch", minable=False, can_collide=False))
    
    _place_tile("oak_leaves_covered_trunk", x, y-2)
    _place_tile("oak_dark_leaves", x, y-3)

    for i in range(y-3, y-1):
        _place_tile("oak_dark_leaves", x-1, i)
    for i in range(y-3, y-1):
        _place_tile("oak_dark_leaves", x+1, i)

    for i in range(y-3, y-1):
        _place_tile("oak_leaves", x-2, i)
    for i in range(y-3, y-1):
        _place_tile("oak_leaves", x+2, i)

    for i in range(x-1, x+2):
        _place_tile("oak_leaves", i, y-4)


def generate_snowy_tree(map, x, y, height):
    pass