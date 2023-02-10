import pygame

class Player:
    def __init__(self, global_instance):
        self.global_instance = global_instance
        
        self.position = pygame.Vector2(0, 0)
        self.original_position = pygame.Vector2(0, 0)
        self.destination = pygame.Vector2(0, 0)
        
    def tick(self):
        self.global_instance.screen.blit(self.global_instance.textures["drill"], self.position * 16)

        if self.position != self.destination:
            self.position = self.position + ((self.destination - self.original_position) / 10)
            return

        self.original_position.x = self.position.x
        self.original_position.y = self.position.y

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.destination.y -= 1
            self.original_position.y = self.position.y
            return

        if keys[pygame.K_DOWN]:
            self.destination.y += 1
            self.original_position.y = self.position.y
            return

        if keys[pygame.K_RIGHT]:
            self.destination.x += 1
            self.original_position.x = self.position.x
            return

        if keys[pygame.K_LEFT]:
            self.destination.x -= 1
            self.original_position.x = self.position.x
            return
