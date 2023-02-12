import pygame, sys
from Classes.map import Map

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((512, 512))
        self.clock = pygame.time.Clock()

        self.map = Map()

        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.map.run()
            pygame.display.update()