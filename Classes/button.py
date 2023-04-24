from typing import Any
import pygame
from pygame import Rect, Surface

from .constants import screen

# Déclaration de la classe Button
class Button():
    """
    Class qui représente un bouton cliquable
    """
    
    def __init__(self, rect: Rect, image: Surface, anim: Surface, text: str, text_size: int, func: callable, parameter: Any = None):
        """
        Initialise un bouton. 
        Prends en paramètres un rectangle où le bouton sera affiché,
        une image et une image d'animation, du texte, la taille du texte,
        une fonction qui sera appelé lorsque l'utilisateur clique sur le bouton
        et un paramètre optionnel qui sera celui de la fonction
        """

        self.rect: Rect = rect
        self.image: Surface = image
        self.anim: Surface = anim
        self.text: str = text
        self.text_size: int = text_size
        self.func: callable = func
        self.parameter: Any = parameter
        self.hovered: bool = False

    def render_text(self) -> None:
        if self.text != "":
            police = pygame.font.Font('prstart.ttf', self.text_size)
            text = police.render(self.text,1,(255,255,255))
            text_shadow = police.render(self.text,1,(50,50,50))
            pos = (self.rect.center[0] - text.get_rect()[2] / 2, self.rect.center[1] - text.get_rect()[3] / 2)
            screen.blit(text_shadow, (pos[0] + 5, pos[1] + 5))
            screen.blit(text, pos)

    def check_event(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.on_click(event)
        self.is_hovered()
        self.update()

    def on_click(self, event) -> None:
        if self.rect.collidepoint(event.pos):
            if self.parameter is None:
                self.func()
            else:
                self.func(self.parameter)

    def is_hovered(self) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
        else:
            self.hovered = False

    def update(self) -> None:
        if not self.hovered:
            screen.blit(self.image, self.rect)
        if self.hovered:
            screen.blit(self.anim, self.rect)
        self.render_text()
