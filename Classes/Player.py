import pygame
from Classes.Constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position, map):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load("Images/Player/Drill_right.png"), (32, 32))
        self.rect = self.image.get_rect()

        self.position = pygame.Vector2(position)
        self.rect.topleft = self.position * 32

        self.moving = 1
        self.falling = False
        self.going_up = False

        self.map = map

    def update(self):

        if self.moving < 1:
            self.moving += 0.5

        self.mine()
        self.fall()

        self.rect.topleft = self.position * 32

        if not self.falling and self.moving >= 1:
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
        current_tile = self.map.tiles[self.position.x][self.position.y]
        if current_tile.type in PLAINS_BLOCKS:
            current_tile.type = "cave"
        if current_tile.type in DESERT_BLOCKS:
            current_tile.type = "sandstone_cave"

    def fall(self):
        tile_below = self.map.tiles[self.position.x][self.position.y + 1]
        if tile_below.type in NOT_A_BLOCK:
            self.falling = True
            self.position.y += 1
        else:
            self.falling = False

    def climb(self):
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
