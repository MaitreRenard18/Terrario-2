import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)

        self.image = pygame.transform.scale(pygame.image.load("Images/PLayer/Drill.png"), (32, 32))
        self.rect = self.image.get_rect()

        self.position = pygame.Vector2(position)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.position.y -= 1

        if keys[pygame.K_DOWN]:
            self.position.y += 1

        if keys[pygame.K_RIGHT]:
            self.position.x += 1

        if keys[pygame.K_LEFT]:
            self.position.x -= 1

        self.rect.center = self.position * 16