import pygame
from Classes.tile import Scaffolding

class Player(pygame.sprite.Sprite):

    def __init__(self, position, map):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load("Images/Player/Drill_right.png"), (32, 32))
        self.tip = pygame.transform.scale(pygame.image.load("Images/Player/DrillTip_right.png"), (32, 32))
        self.rect = self.image.get_rect()

        self.original_pos = pygame.Vector2(position)
        self.position = pygame.Vector2(position)
        self.destination = pygame.Vector2(position)
        self.rect.topleft = self.position * 32

        self.going = {"direction": "right", "tip_tile": (1, 0)}
        self.falling = None
        self.tile_below = None

        self.map = map

    def update(self):

        self.rect.topleft = self.position * 32
        pygame.sprite.Sprite.update(self)
        
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
                return
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_g]:
                self.map.set_tile(Fluid(self.map, self.position.copy(), "water", "water", 1), self.position.copy())

            if keys[pygame.K_UP]:
                self.destination.y -= 1
                self.going["direction"], self.going["tip_tile"] = "up", (0, -1)
                return

            if keys[pygame.K_DOWN]:
                self.destination.y += 1
                self.going["direction"], self.going["tip_tile"] = "down", (0, 1)
                return

            if keys[pygame.K_RIGHT]:
                self.destination.x += 1
                self.going["direction"], self.going["tip_tile"] = "right", (1, 0)
                return

            if keys[pygame.K_LEFT]:
                self.destination.x -= 1
                self.going["direction"], self.going["tip_tile"] = "left", (-1, 0)
                return

    def mine(self):
        current_tile = self.map.get_tile(self.destination)
        current_tile.destroy()

    def fall(self):
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

    def get_lowest_dest(self):
        self.tile_below = self.map.get_tile(self.destination + (0, 1))
        if not self.tile_below.can_collide:
            self.destination.y += 1
            self.get_lowest_dest()
        return

    def climb(self):
        self.tile_below = self.map.get_tile(self.destination + (0, 1))
        self.map._tiles[self.destination.x][self.destination.y + 1] = Scaffolding(self.tile_below.texture)
            
    def facing(self, direction):
        self.image = pygame.transform.scale(pygame.image.load(f"Images/Player/Drill_{direction}.png"), (32, 32))
        self.tip = pygame.transform.scale(pygame.image.load(f"Images/Player/DrillTip_{direction}.png"), (32, 32))
