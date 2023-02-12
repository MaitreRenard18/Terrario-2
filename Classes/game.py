import pygame, sys
from Classes.map import Map

class Game:
    def __init__(self):
        """Initialise la fenêtre Pygame et les différentes instances nécessaires au jeu."""

        pygame.init()
        self.screen = pygame.display.set_mode((512, 512))
        self.clock = pygame.time.Clock()

        self.map = Map()

        self.run()

    def run(self):
        """Commence la boucle d'execution."""

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.map.update()
            pygame.display.update()
            self.clock.tick(30)