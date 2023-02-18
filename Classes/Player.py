import pygame
import math
from Classes.Constants import *

def falling_position(elapsed, initial_velocity, initial_y):
    """
    Gravity handling

    Acceleration: GRAVITY
    Velocity: GRAVITY * t + v0
    Position: ((GRAVITY * t)^2)/2 + v0t + y0
    """
    return math.pow(GRAVITY * elapsed, 2) + start_velocity * elapsed + start_y

class Player(pygame.sprite.Sprite):
    def __init__(self, position, map):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load("Images/Player/Drill_right.png"), (32, 32))
        self.rect = self.image.get_rect()

        self.position = pygame.Vector2(position)
        self.rect.topleft = self.position * 32

        self.moving = 1
        self.going_up = False

        # Store the elapsed time, the initial position and velocity when the
        # player started falling
        self.falling = None

        self.map = map

    def update(self):
        if self.moving < 1:
            self.moving += 0.5

        self.mine()
        self.fall()

        self.rect.topleft = self.position * 32

        if self.falling == None and self.moving >= 1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.position.y -= 1
                self.going_up = True
                self.facing("up")
                return

            if keys[pygame.K_DOWN]:
                self.position.y += 1
                self.facing("down")
                return

            if keys[pygame.K_RIGHT]:
                self.position.x += 1
                self.facing("right")
                return

            if keys[pygame.K_LEFT]:
                self.position.x -= 1
                self.facing("left")
                return

    def mine(self):
        if self.falling == None:
            current_tile = self.map.tiles[self.position.x][self.position.y]
            if current_tile.type in PLAINS_BLOCKS:
                current_tile.type = "cave"
            if current_tile.type in DESERT_BLOCKS:
                current_tile.type = "sandstone_cave"

    def fall(self):
        tile_below = self.map.tiles[self.position.x][self.position.y + 1]
        if tile_below.type in NOT_A_BLOCK:
            if self.falling == None:
                self.falling = { "elapsed": 0, "initial_velocity": self.moving, "initial_y": self.position.y }

            # "**" means that the object is destructured into its fields, in
            # other words, the fields of the object are passed as arguments
            #
            # We also need to avoid moving more than one tile at a time
            self.position.y = round(min(self.position.y + 1, falling_position(**self.falling)))
            self.falling["elapsed"] += 1
        else:
            self.falling = None

    def climb(self):
        if self.falling == None:
            tile_above = self.map.tiles[self.position.x][self.position.y + 1]
            if tile_above.type in SURFACE_TILES:
                tile_above.type = "scaffolding"
            if tile_above.type in PLAINS_TILES:
                tile_above.type = "scaffolding_stone"
            if tile_above.type in DESERT_TILES:
                tile_above.type = "scaffolding_sandstone"

        self.going_up = False

    def facing(self, direction):
        self.image = pygame.transform.scale(pygame.image.load(f"Images/Player/Drill_{direction}.png"), (32, 32))
        self.moving = 0
