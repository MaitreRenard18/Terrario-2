import sys

import pygame


class Game:
    def __init__(self):
        """Initialise la fenêtre Pygame et les différentes instances nécessaires au jeu."""

        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

        flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode(flags=flags)
        self.clock = pygame.time.Clock()

        from Classes.map import Map
        self.map = Map()

        self.run()

    def run(self):
        """Commence la boucle d'execution."""

        show_fps = False
        max_fps = 30

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
                    show_fps = not show_fps

                if event.type == pygame.KEYDOWN and event.key == pygame.K_F2:
                    max_fps = 120 if max_fps == 60 else 60 if max_fps == 30 else 30

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.map.update()

            if show_fps:
                font = pygame.font.SysFont("Arial Bold", 48)
                img = font.render(f"FPS: {round(self.clock.get_fps())}", True, pygame.Color(255, 0, 0))
                pygame.display.get_surface().blit(img, (0, 0))

            pygame.display.update()
            self.clock.tick(max_fps)
