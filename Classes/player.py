import pygame
from Classes.tile import Scaffolding, Fluid

class Player(pygame.sprite.Sprite):
    def __init__(self, position, map):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load("Images/Tiles/Air.png"), (32, 32))
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


        self.rect.topleft = self.position * 32

        if not self.falling and self.moving >= 1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_g]:
                print("Placed water")
                self.map.set_tile(Fluid(self.map, self.position.copy(), "water", "water", 25), self.position.x, self.position.y)

            if keys[pygame.K_a]:
                print(self.map.get_tile(self.position.x, self.position.y).can_collide)

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

        self.mine()
        self.fall()

    def mine(self):
        current_tile = self.map.tiles[self.position.x][self.position.y]
        current_tile.mine()

    def fall(self):
        tile_below = self.map.tiles[self.position.x][self.position.y + 1]
        if not tile_below.can_collide:
            self.falling = True
            self.position.y += 1
        else:
            self.falling = False

    def climb(self):
        tile_above = self.map.tiles[self.position.x][self.position.y + 1]
        self.map.tiles[self.position.x][self.position.y + 1] = Scaffolding(tile_above.type, tile_above.texture)
        
        self.going_up = False

    def facing(self, direction):
        #self.image = pygame.transform.scale(pygame.image.load(f"Images/PLayer/Drill_{direction}.png"), (32, 32))
        self.moving = 0
