import pygame
from Classes.tile import Scaffolding

class Player(pygame.sprite.Sprite):

    def __init__(self, position, map):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load("Images/PLayer/Drill_right.png"), (32, 32))
        self.tip = pygame.transform.scale(pygame.image.load("Images/PLayer/DrillTip_right.png"), (32, 32))
        self.rect = self.image.get_rect()

        self.original_pos = pygame.Vector2(position)
        self.position = pygame.Vector2(position)
        self.destination = pygame.Vector2(position)
        self.rect.topleft = self.position * 32

        self.going = ["right", (1,0)]
        self.falling = None

        self.map = map

    def update(self):

        self.rect.topleft = self.position * 32
        pygame.sprite.Sprite.update(self)

        self.mine()
        #self.fall() Je désactive la gravité, parce qu'elle bug

        if self.position != self.destination:
            self.position += (self.destination - self.original_pos) / 5
            return
        
        self.original_pos.x = self.position.x
        self.original_pos.y = self.position.y

        if self.falling == None:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.destination.y -= 1
                self.original_pos.y = self.position.y
                self.going = ["up", (0, -1)]
                return

            if keys[pygame.K_DOWN]:
                self.destination.y += 1
                self.original_pos.y = self.position.y
                self.going = ["down", (0, 1)]
                return

            if keys[pygame.K_RIGHT]:
                self.destination.x += 1
                self.original_pos.x = self.position.x
                self.going = ["right", (1, 0)]
                return

            if keys[pygame.K_LEFT]:
                self.destination.x -= 1
                self.original_pos.x = self.position.x
                self.going = ["left", (-1, 0)]
                return

    def mine(self):
        current_tile = self.map.get_tile(self.destination)
        current_tile.destroy()

    def fall(self):
        tile_below = self.map.get_tile((self.destination.x, self.destination.y + 1))
        if not tile_below.can_collide:
            if self.falling is None:
                self.falling = 0.5

            self.destination.y += round(self.falling)
            self.falling += 0.15

        else:
            self.falling = None

    def climb(self):
        tile_below = self.map.get_tile(self.destination)
        self.map._tiles[self.destination.x][self.destination.y + 1] = Scaffolding(tile_below.type, tile_below.texture)
            
    def facing(self, direction):
        self.image = pygame.transform.scale(pygame.image.load(f"Images/PLayer/Drill_{direction[0]}.png"), (32, 32))
        self.tip = pygame.transform.scale(pygame.image.load(f"Images/PLayer/DrillTip_{direction[0]}.png"), (32, 32))
