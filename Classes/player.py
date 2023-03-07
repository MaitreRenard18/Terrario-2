from typing import Union, Dict, Callable

import pygame
from pygame import Vector2, Surface, Rect, transform, image, display

from Classes.tile import Tile, Scaffolding

class Player(pygame.sprite.Sprite):

    def __init__(self, position, map) -> None:
        super().__init__()

        self.image: Surface = pygame.transform.scale(pygame.image.load("Images/Player/Drill_right.png"), (32, 32))
        self.tip: Surface = pygame.transform.scale(pygame.image.load("Images/Player/DrillTip_right.png"), (32, 32))
        self.rect: Rect = self.image.get_rect()

        self.original_pos: Vector2 = pygame.Vector2(position)
        self.position: Vector2 = pygame.Vector2(position)
        self.destination: Vector2 = pygame.Vector2(position)
        self.rect.topleft: tuple = self.position * 32

        self.move: Dict[str, Union[str, tuple, bool]] = {"direction": "right", "tip_tile": (1, 0), "going_down": False}
        self.falling: Union[None, float] = None
        self.tile_below: Tile = None

        self.map = map

    def update(self) -> None:

        self.rect.topleft = self.position * 32
        pygame.sprite.Sprite.update(self)
        
        if self.move["going_down"]:
            pass
        else:
            self.fall()

        if self.falling is None:

            self.mine()

            if self.position != self.destination:
                self.position += (self.destination - self.original_pos) / 5
                return
            
            if self.original_pos != self.position:
                self.position.x = round(self.position.x)
                self.position.y = round(self.position.y)
                self.original_pos.x = self.position.x
                self.original_pos.y = self.position.y
                self.move["going_down"] = False
                return
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.destination.y -= 1
                self.move["direction"], self.move["tip_tile"] = "up", (0, -1)
                return

            if keys[pygame.K_DOWN]:
                self.destination.y += 1
                self.move["direction"], self.move["tip_tile"] = "down", (0, 1)
                if not self.move["going_down"]:
                    self.move["going_down"] = True
                return

            if keys[pygame.K_RIGHT]:
                self.destination.x += 1
                self.move["direction"], self.move["tip_tile"] = "right", (1, 0)
                return

            if keys[pygame.K_LEFT]:
                self.destination.x -= 1
                self.move["direction"], self.move["tip_tile"] = "left", (-1, 0)
                return

    def mine(self) -> None:
        dest_tile = self.map.get_tile(self.destination)
        dest_tile.destroy()

    def fall(self) -> None:
        self.tile_below = self.map.get_tile(self.original_pos + (0, 1))
        if not self.tile_below.can_collide:
            if self.falling is None:
                self.falling = 0
                self.get_lowest_dest()

            self.position.y += self.falling
            if self.falling < 2:
                self.falling += 0.05
            else:
                self.falling = round(self.falling)

            if self.position.y >= self.destination.y:
                self.original_pos.y = self.destination.y
                self.position.y = self.destination.y
        else:
            self.falling = None

    def get_lowest_dest(self) -> None:
        self.tile_below = self.map.get_tile(self.destination + (0, 1))
        if not self.tile_below.can_collide:
            self.destination.y += 1
            self.get_lowest_dest()
        return

    def climb(self) -> None:
        self.tile_below = self.map.get_tile(self.destination + (0, 1))
        self.map._tiles[self.destination.x][self.destination.y + 1] = Scaffolding(self.tile_below.type, self.tile_below.texture)
            
    def facing(self, direction: str) -> None:
        self.image = pygame.transform.scale(pygame.image.load(f"Images/Player/Drill_{direction}.png"), (32, 32))
        self.tip = pygame.transform.scale(pygame.image.load(f"Images/Player/DrillTip_{direction}.png"), (32, 32))
