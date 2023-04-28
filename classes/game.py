import sys

import pygame
from pygame import Surface, time

from .menu import Menu
from .map import Map
from .saving import save
from .constants import font


class Game:
    def __init__(self):
        """Initialise la fenêtre Pygame et les différentes instances nécessaires au jeu."""

        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

        flags: int = pygame.FULLSCREEN | pygame.DOUBLEBUF
        self.screen: Surface = pygame.display.set_mode(flags=flags)
        self.clock: time.Clock = time.Clock()

        self.map: Map = Map()
        self.menu: Menu = Menu(self.map)

        self.run()

    def run(self) -> None:
        """Commence la boucle d'execution."""

        show_stats: bool = False
        max_fps: int = 30

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
                    show_stats = not show_stats

                if event.type == pygame.KEYDOWN and event.key == pygame.K_F2:
                    max_fps = 120 if max_fps == 60 else 60 if max_fps == 30 else 30

                if event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
                    self.map.player.level = (self.map.player.level % 7) + 1

                if event.type == pygame.QUIT:
                    if not self.menu.displayed:
                        save(self.menu.save_name, self.menu.map)
                    pygame.quit()
                    sys.exit()
               
            if self.menu.displayed:
                self.menu.update(event)
            else:
                self.map: Map = self.menu.map
                self.map.update()
            
                if self.map.player.display_button:
                    self.map.player.upgrade_button.check_event(event)
            
            self.menu.quit_button.check_event(event)

            if show_stats:

                fps: Surface = font.render(f"FPS: {round(self.clock.get_fps())}", True, (255, 255, 255))
                pygame.display.get_surface().blit(fps, (2, 0))

                position: Surface = font.render(f"Position: {self.menu.map.player.position}",
                                       True, (255, 255, 255))
                pygame.display.get_surface().blit(position, (2, 32))

                level: Surface = font.render(f"Drill level: {self.menu.map.player.level}", True, (255, 255, 255))
                pygame.display.get_surface().blit(level, (2, 64))

            pygame.display.flip()
            self.clock.tick(max_fps)
